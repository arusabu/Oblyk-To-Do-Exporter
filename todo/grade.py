from todo.models import Route


def filter_routes(
    routes: list[Route],
    grade_min_value: int,
    grade_max_value: int,
) -> list[Route]:
    return [
        route
        for route in routes
        if grade_min_value <= route.grade_value <= grade_max_value
    ]