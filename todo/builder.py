from collections import defaultdict
from collections.abc import Iterable

from todo.models import Ascent, Route, RouteHistory


def build_route_ascents(
    routes: Iterable[Route],
    ascents: Iterable[Ascent],
) -> dict[int, list[Ascent]]:
    route_ids = {
        route.id
        for route in routes
    }

    route_ascents: dict[int, list[Ascent]] = defaultdict(list)

    for ascent in ascents:
        if ascent.route_id not in route_ids:
            continue

        route_ascents[ascent.route_id].append(ascent)

    return dict(route_ascents)

def build_route_history(
    ascents: Iterable[Ascent],
) -> RouteHistory:
    worked = False
    top_rope_count = 0
    lead_count = 0
    unknown_roping_count = 0

    for ascent in ascents:
        if ascent.ascent_status == "project":
            worked = True
            continue

        if ascent.roping_status == "top_rope":
            top_rope_count += ascent.quantity
        elif ascent.roping_status == "lead_climb":
            lead_count += ascent.quantity
        else:
            unknown_roping_count += ascent.quantity

    return RouteHistory(
        worked=worked,
        top_rope_count=top_rope_count,
        lead_count=lead_count,
        unknown_roping_count=unknown_roping_count,
    )

def needs_top_rope(
    history: RouteHistory,
) -> bool:
    return not history.is_completed


def needs_lead(
    route: Route,
    history: RouteHistory,
) -> bool:
    return (
        not route.is_auto_belay
        and not history.has_lead
    )