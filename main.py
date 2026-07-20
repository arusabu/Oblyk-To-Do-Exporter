import console
import os
from config import load_config
from datetime import date
from dotenv import load_dotenv
from exporters.ods import export_todo_ods
from oblyk.client import build_space_order, OblykClient
from pathlib import Path
from time import perf_counter
from todo.builder import (
    build_route_ascents,
    build_route_history,
    needs_lead,
    needs_top_rope,
)
from todo.grade import GradeScale, filter_routes
from todo.models import Ascent, Route

start = perf_counter()

config = load_config()

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

    console.blank()
    console.title("Oblyk To-Do Exporter 0.1.0")
    console.blank()

    console.info("Connexion à Oblyk...")
    client.login(
        email=email,
        password=password,
    )
    console.success("Authentifié.")

    gym_id = config.gym.id

    current_user = client.get_current_user()
    user_name = current_user.get("full_name") or "?"
    console.blank()
    console.info(f"Salut {user_name} !")
    console.blank()

    console.info("Récupération des espaces...")
    spaces = client.get_gym_spaces(gym_id)
    console.success(f"{len(spaces)} espace(s) trouvé(s).")

    console.blank()
    console.info("Téléchargement des voies...")
    route_data = client.get_current_gym_routes(gym_id)
    
    routes = [
        Route.from_api(data)
        for data in route_data
        if data.get("climbing_type") == "sport_climbing"
        and not data.get("dismounted", False)
    ]

    route_counts: dict[str, int] = {}

    console.success(
        f"{len(routes)} voie(s) sportive(s) disponible(s)."
    )

    console.blank()
    console.info("Répartition par espace :")
    space_order = build_space_order(spaces)

    for route in routes:
        route_counts[route.space] = (
            route_counts.get(route.space, 0) + 1
        )

    label_width = (
        max(len(space["name"]) for space in spaces) + 5
    )

    for space in spaces:
        name = space["name"].strip()
        count = route_counts.get(name, 0)
        if count == 0:
            continue
        console.item(name, count, label_width)

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

    session_data = client.get_climbing_sessions()

    gym_sessions = [
        session
        for session in session_data
        if gym_id in (session.get("gyms") or [])
        and date.fromisoformat(session["session_date"]) >= oldest_route_date
    ]

    ascents: list[Ascent] = []

    for index, session in enumerate(gym_sessions, start=1):
        session_date_raw = session["session_date"]
        session_date = date.fromisoformat(session_date_raw)

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

    console.blank()
    console.success("Document créé :")
    console.info(f"  {output_path}")
    console.blank()
    elapsed = perf_counter() - start
    console.info(f"Terminé en {elapsed:.1f} s.")
    console.blank()

if __name__ == "__main__":
    main()