from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class Route:
    id: int
    name: str
    space: str
    sector: str
    grade: str
    grade_value: int
    hold_colors: tuple[str, ...]
    opened_at: date
    openers: tuple[str, ...]
    is_auto_belay: bool

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Route":
        sections = data.get("sections") or []
        section = sections[0] if sections else {}

        space = (
            data.get("gym_space", {}).get("name") or "?"
        ).strip()

        sector = (
            data.get("gym_sector", {}).get("name") or "?"
        ).strip()

        name = (data.get("name") or "?").strip()
        grade = (section.get("grade") or "?").strip()
        grade_value = section.get("grade_value")

        if grade_value is None:
            grade_value = -1

        hold_colors = tuple(
            color
            for color in data.get("hold_colors") or []
            if color
        )

        openers = tuple(
            (opener.get("name") or "?").strip()
            for opener in data.get("openers") or []
        )

        opened_at_raw = data.get("opened_at")

        if not opened_at_raw:
            raise ValueError(
                f"Route {data.get('id')} has no opening date"
            )

        return cls(
            id=data["id"],
            name=name,
            space=space,
            sector=sector,
            grade=grade,
            grade_value=grade_value,
            hold_colors=hold_colors,
            opened_at=date.fromisoformat(opened_at_raw),
            openers=openers,
            is_auto_belay=sector.casefold().startswith("enrouleur"),
        )

    @property
    def display_sector(self) -> str:
        if not self.is_auto_belay:
            return self.sector

        number = self.sector[len("Enrouleur"):].strip()

        if not number:
            return "AUTO"

        return f"AUTO {number}"

@dataclass(frozen=True)
class Ascent:
    route_id: int
    session_date: date
    ascent_status: str
    roping_status: str | None
    quantity: int

    @classmethod
    def from_api(
        cls,
        data: dict[str, Any],
        session_date: date,
    ) -> "Ascent":
        quantity = data.get("quantity") or 1

        return cls(
            route_id=data["gym_route_id"],
            session_date=session_date,
            ascent_status=data.get("ascent_status") or "?",
            roping_status=data.get("roping_status"),
            quantity=quantity,
        )

@dataclass(frozen=True)
class RouteHistory:
    worked: bool
    top_rope_count: int
    lead_count: int
    unknown_roping_count: int

    @property
    def has_top_rope(self) -> bool:
        return self.top_rope_count > 0

    @property
    def has_lead(self) -> bool:
        return self.lead_count > 0

    @property
    def has_unknown_roping(self) -> bool:
        return self.unknown_roping_count > 0

    @property
    def is_completed(self) -> bool:
        return (
            self.has_top_rope
            or self.has_lead
            or self.has_unknown_roping
        )