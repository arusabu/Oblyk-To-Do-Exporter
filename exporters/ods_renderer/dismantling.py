from datetime import date

from todo.models import Route

from .constants import (
    DISMANTLING_WARNING_THRESHOLD,
    DISMANTLING_CRITICAL_THRESHOLD,
)

def get_dismantling_indicator(
    route: Route,
    all_routes_in_space: list[Route],
    today: date,
) -> str:

    if len(all_routes_in_space) < 2:
        return ""

    oldest_route = min(
        all_routes_in_space,
        key=lambda r: r.opened_at,
    )

    oldest_age = (
        today - oldest_route.opened_at
    ).days

    if oldest_age <= 0:
        return ""

    current_age = (
        today - route.opened_at
    ).days

    ratio = current_age / oldest_age

    if ratio >= DISMANTLING_CRITICAL_THRESHOLD:
        return "critical"

    if ratio >= DISMANTLING_WARNING_THRESHOLD:
        return "warning"

    return ""