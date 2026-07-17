from __future__ import annotations

from .constants import (
    GRADE_COLORS,
    WHITE_MIX,
)

def normalize_grade(grade: str) -> str:
    normalized = grade.strip().casefold().rstrip("+")
    if len(normalized) == 1 and normalized.isdigit():
        return normalized + "a"
    return normalized

def mix_with_white(
    color: str,
    amount: float = WHITE_MIX,
) -> str:
    color = color.lstrip("#")
    red = int(color[0:2], 16)
    green = int(color[2:4], 16)
    blue = int(color[4:6], 16)
    red = round(red + (255 - red) * amount)
    green = round(green + (255 - green) * amount)
    blue = round(blue + (255 - blue) * amount)
    return f"#{red:02x}{green:02x}{blue:02x}"

def grade_background(grade: str) -> str:
    color = GRADE_COLORS.get(normalize_grade(grade))
    if color is None:
        return "#ffffff"
    return mix_with_white(color)