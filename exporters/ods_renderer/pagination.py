from todo.models import Route
from .constants import HOLD_COLOR_ORDER
from .helpers import format_sector

def hold_color_sort_key(route: Route) -> int:
    if not route.hold_colors:
        return 999

    return HOLD_COLOR_ORDER.get(
        route.hold_colors[0].casefold(),
        999,
    )

def route_sort_key(route: Route):
    return (
        route.grade_value,
        format_sector(route.display_sector),
        hold_color_sort_key(route),
        route.name.casefold(),
    )


def paginate_routes(
    routes: list[Route],
    first_page_rows: int,
    continuation_rows: int,
) -> list[list[Route]]:
    if not routes:
        return []

    pages: list[list[Route]] = []

    index = 0

    pages.append(routes[:first_page_rows])
    index = first_page_rows

    while index < len(routes):
        pages.append(
            routes[index:index + continuation_rows]
        )
        index += continuation_rows

    return pages