from __future__ import annotations

WHITE_MIX = 0.65

GRADE_COLORS = {
    "3a": "#ffdd54",
    "3b": "#f9d033",
    "3c": "#f3c311",
    "4a": "#ff7f2a",
    "4b": "#ee6e19",
    "4c": "#dd5d08",
    "5a": "#aad400",
    "5b": "#8fb200",
    "5c": "#739000",
    "6a": "#0055d4",
    "6b": "#0040a1",
    "6c": "#002c6e",
    "7a": "#ab37c8",
    "7b": "#902ea8",
    "7c": "#752588",
    "8a": "#ff3b3b",
    "8b": "#dd1919",
}

HOLD_COLOR_ORDER = {
    "#ffcc00": 0,   # jaune
    "#2ca02c": 1,   # vert
    "#0055d4": 2,   # bleu
    "#ab37c8": 3,   # violet
    "#ff0000": 4,   # rouge
    "#f2f2f2": 5,   # blanc
    "#1a1a1a": 6,   # noir
}

DISMANTLING_COLORS = {
   "warning" : "#FFA500", 
   "critical" : "#b00020",
}

DISMANTLING_WARNING_THRESHOLD = 0.70
DISMANTLING_CRITICAL_THRESHOLD = 0.85

ROUTE_STYLE_TYPES = (
    "normal",
    "centered",
    "warning",
    "centered_warning",
    "critical",
    "centered_critical",
    "grade",
)

HEADERS = (
    "",
    "Secteur",
    "Cot.",
    "Prises",
    "Voie",
    "Ouvreur",
    "Ouverte le",
    "",
    "État",
)

COLUMN_WIDTHS = (
    "1.50cm",
    "2.00cm",
    "1.50cm",
    "1.50cm",
    "11.00cm",
    "4.00cm",
    "2.50cm",
    "1.00cm",
    "2.50cm",
)

FIRST_PAGE_ROWS = 28
CONTINUATION_PAGE_ROWS = 30