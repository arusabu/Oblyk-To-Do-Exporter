import os
from config import load_config
from datetime import date
from dotenv import load_dotenv
from exporters.ods import export_todo_ods
from oblyk.client import build_space_order, OblykClient
from pathlib import Path
from todo.builder import (
    build_route_ascents,
    build_route_history,
    needs_lead,
    needs_top_rope,
)
from todo.grade import GradeScale, filter_routes
from todo.models import Ascent, Route

config = load_config()

print(config)

def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return value


def main() -> None:
    load_dotenv()

    email = get_required_env("OBLYK_EMAIL")
    password = get_required_env("OBLYK_PASSWORD")

    client = OblykClient()

    client.login(
        email=email,
        password=password,
    )

    gym_id = config.gym.id

    current_user = client.get_current_user()
    user_name = current_user.get("full_name") or "?"
    route_data = client.get_current_gym_routes(gym_id)
    spaces = client.get_gym_spaces(gym_id)
    space_order = build_space_order(spaces)

    routes = [
        Route.from_api(data)
        for data in route_data
        if data.get("climbing_type") == "sport_climbing"
        and not data.get("dismounted", False)
    ]

    grade_scale = GradeScale(routes)

    top_rope_min, top_rope_max = grade_scale.validate_range(
        config.top_rope.grade_min,
        config.top_rope.grade_max,
    )

    lead_min, lead_max = grade_scale.validate_range(
        config.lead.grade_min,
        config.lead.grade_max,
    )

    if not routes:
        raise RuntimeError("No current sport climbing routes found")

    oldest_route_date = min(
        route.opened_at
        for route in routes
    )

    print()
    print(
        f"[INFO] {len(route_data)} current route(s) fetched, "
        f"{len(routes)} sport climbing route(s) retained."
    )
    print(
        f"[INFO] Oldest current route opened on "
        f"{oldest_route_date.isoformat()}."
    )
    print()

    session_data = client.get_climbing_sessions()

    gym_sessions = [
        session
        for session in session_data
        if gym_id in (session.get("gyms") or [])
        and date.fromisoformat(session["session_date"]) >= oldest_route_date
    ]

    print()
    print(
        f"[INFO] {len(session_data)} climbing session(s) fetched, "
        f"{len(gym_sessions)} relevant session(s) retained "
        f"for gym {gym_id}."
    )
    print()

    ascents: list[Ascent] = []

    for index, session in enumerate(gym_sessions, start=1):
        session_date_raw = session["session_date"]
        session_date = date.fromisoformat(session_date_raw)

        print(
            f"[INFO] Fetching session details "
            f"[{index}/{len(gym_sessions)}]..."
        )

        detail = client.get_climbing_session(session_date_raw)

        for ascent_data in detail.get("gym_ascents") or []:
            gym = ascent_data.get("gym") or {}

            if gym.get("id") != gym_id:
                continue

            if ascent_data.get("climbing_type") != "sport_climbing":
                continue

            ascents.append(
                Ascent.from_api(
                    ascent_data,
                    session_date=session_date,
                )
            )

    route_ascents = build_route_ascents(
        routes=routes,
        ascents=ascents,
    )

    top_rope_routes = filter_routes(
        routes,
        top_rope_min,
        top_rope_max,
    )

    lead_routes = filter_routes(
        routes,
        lead_min,
        lead_max,
    )

    top_rope_todo: list[Route] = []

    for route in top_rope_routes:
        history = build_route_history(
            route_ascents.get(route.id, [])
        )

        if needs_top_rope(history):
            top_rope_todo.append(route)

    lead_todo: list[Route] = []

    for route in lead_routes:
        history = build_route_history(
            route_ascents.get(route.id, [])
        )

        if needs_lead(route, history):
            lead_todo.append(route)

    print()
    print("========================")
    print("Top-rope to-do")
    print("========================")
    print()

    for route in top_rope_todo:
        history = build_route_history(
            route_ascents.get(route.id, [])
        )

        status = "PROJECT" if history.worked else "UNTRIED"

        print(
            f"{route.space} | "
            f"{route.display_sector} | "
            f"{route.grade} | "
            f"{status} | "
            f"{route.name}"
        )

    print()
    print(
        f"[INFO] {len(top_rope_todo)} route(s) "
        f"in top-rope to-do."
    )

    print()
    print("========================")
    print("Lead to-do")
    print("========================")
    print()

    for route in lead_todo:
        history = build_route_history(
            route_ascents.get(route.id, [])
        )

        if history.has_top_rope:
            status = "TOP ROPE DONE"
        elif history.has_unknown_roping:
            status = "COMPLETED - ROPING UNKNOWN"
        elif history.worked:
            status = "PROJECT"
        else:
            status = "UNTRIED"

        print(
            f"{route.space} | "
            f"{route.display_sector} | "
            f"{route.grade} | "
            f"{status} | "
            f"{route.name}"
        )

    print()
    print(
        f"[INFO] {len(lead_todo)} route(s) "
        f"in lead to-do."
    )

    generated_at = date.today()
    output_path = Path("output") / "oblyk-todo.ods"

    export_todo_ods(
        output_path=output_path,
        all_routes=routes,
        top_rope_routes=top_rope_todo,
        lead_routes=lead_todo,
        route_ascents=route_ascents,
        user_name=user_name,
        generated_at=generated_at,
        top_rope_grade_min=config.top_rope.grade_min,
        top_rope_grade_max=config.top_rope.grade_max,
        lead_grade_min=config.lead.grade_min,
        lead_grade_max=config.lead.grade_max,
        space_order=space_order,
    )

    print()
    print(
        f"[INFO] ODS exported to {output_path}."
    )

if __name__ == "__main__":
    main()