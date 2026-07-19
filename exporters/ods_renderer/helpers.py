from datetime import date

from todo.models import Route


def format_sector(sector: str) -> str:
    normalized = sector.strip()

    if normalized.isdigit():
        return normalized.zfill(2)

    if normalized.upper().startswith("AUTO "):
        auto_number = normalized[5:].strip()

        if auto_number.isdigit():
            return f"Auto {auto_number.zfill(2)}"

    return normalized


def format_space(space: str) -> str:
    return space.strip().upper()


def is_rotation_warning(
    route: Route,
    generated_at: date,
) -> bool:
    age_days = (generated_at - route.opened_at).days

    if route.space == "Grande Salle":
        return age_days >= 90
    
    if route.space == "Voie Etage":
        return age_days >= 150

    if route.space == "Mur Extérieur":
        return age_days >= 150

    return False