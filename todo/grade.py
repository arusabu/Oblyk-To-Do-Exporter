from collections.abc import Iterable

from todo.models import Route


class GradeScale:
    """
    Correspondance entre les cotations textuelles ("6a+", "7b"...)
    et les valeurs numériques renvoyées par Oblyk.
    """

    def __init__(self, routes: Iterable[Route]) -> None:

        self._values: dict[str, int] = {}

        for route in routes:

            if route.grade is None:
                continue

            if route.grade_value is None:
                continue

            previous = self._values.get(route.grade)

            if previous is None:

                self._values[route.grade] = route.grade_value

            elif previous != route.grade_value:

                raise ValueError(
                    "Inconsistent grade mapping: "
                    f"{route.grade} -> "
                    f"{previous} / {route.grade_value}"
                )

        self._grades: list[str] = sorted(
            self._values,
            key=lambda grade: self._values[grade],
        )

    def __contains__(self, grade: str) -> bool:
        return grade in self._values

    def __getitem__(self, grade: str) -> int:

        try:
            return self._values[grade]

        except KeyError:

            available = ", ".join(self._grades)

            raise ValueError(
                f"Unknown grade '{grade}'.\n"
                f"Available grades: {available}"
            ) from None

    def grades(self) -> list[str]:
        return self._grades.copy()
    
    def validate_range(
        self,
        minimum: str,
        maximum: str,
    ) -> tuple[int, int]:
        """
        Valide une plage de cotations et renvoie les valeurs numériques
        correspondantes.
        """

        minimum_value = self[minimum]
        maximum_value = self[maximum]

        if minimum_value > maximum_value:
            raise ValueError(
                "Invalid grade range:\n"
                f"minimum = '{minimum}'\n"
                f"maximum = '{maximum}'\n\n"
                "The minimum grade cannot be greater than "
                "the maximum grade."
            )

        return minimum_value, maximum_value

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