from datetime import date

from todo.models import Route

RED_THRESHOLD = 0.85
YELLOW_THRESHOLD = 0.70

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

    RED = "red"
    YELLOW = "yellow"
    NONE = ""

    ratio = current_age / oldest_age

    if ratio >= RED_THRESHOLD:
        return RED

    if ratio >= YELLOW_THRESHOLD:
        return YELLOW

    return NONE