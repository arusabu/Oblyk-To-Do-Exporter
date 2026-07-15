from datetime import date
from pathlib import Path
from typing import Any

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import (
    ParagraphProperties,
    Style,
    TableCellProperties,
    TableColumnProperties,
    TextProperties,
)

from odf.table import (
    Table,
    TableCell,
    TableColumn,
    TableRow,
)

from odf.text import P

from todo.builder import build_route_history
from todo.models import Ascent, Route


GRADE_COLORS = {
    "3": "#ffdd54",
    "4a": "#f9d033",
    "4b": "#f3c311",
    "4c": "#ff7f2a",
    "5a": "#ee6e19",
    "5b": "#dd5d08",
    "5c": "#aad400",
    "6a": "#8fb200",
    "6b": "#739000",
    "6c": "#0055d4",
    "7a": "#0040a1",
    "7b": "#002c6e",
    "7c": "#ab37c8",
    "8a": "#902ea8",
    "8b": "#752588",
    "8c": "#ff3b3b",
    "9a": "#dd1919",
}

WHITE_MIX = 0.85

SPACE_ORDER = {
    "Grande Salle": 0,
    "Voie Etage": 1,
    "Mur Extérieur": 2,
}

HEADERS = (
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
    "2.00cm",
    "1.50cm",
    "1.50cm",
    "10.00cm",
    "3.00cm",
    "2.50cm",
    "1.00cm",
    "2.00cm",
)


def normalize_grade(grade: str) -> str:
    normalized = grade.strip().casefold().rstrip("+")

    if normalized.startswith("3"):
        return "3"

    return normalized

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
    normalized = space.strip()

    names = {
        "Grande Salle": "GRANDE SALLE",
        "Voie Etage": "VOIE ÉTAGE",
        "Mur Extérieur": "MUR EXTÉRIEUR",
    }

    return names.get(
        normalized,
        normalized.upper(),
    )

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


def is_rotation_warning(
    route: Route,
    generated_at: date,
) -> bool:
    age_days = (generated_at - route.opened_at).days

    if route.space == "Grande Salle":
        return age_days >= 90

    if route.space == "Mur Extérieur":
        return age_days >= 150

    return False


def route_sort_key(route: Route) -> tuple[int, int, str]:
    return (
        SPACE_ORDER.get(route.space, 999),
        -route.grade_value,
        route.display_sector.casefold(),
    )


def add_text(
    cell: Any,
    text: str,
    paragraph_style: Any | None = None,
) -> None:
    paragraph = P(
        stylename=paragraph_style,
        text=text,
    )
    cell.addElement(paragraph)

def create_styles(
    document: Any,
) -> dict[str, Any]:
    styles: dict[str, Any] = {}

    title_cell = Style(
        name="TitleCell",
        family="table-cell",
    )
    title_cell.addElement(
        TableCellProperties(
            verticalalign="middle",
        )
    )
    title_cell.addElement(
        ParagraphProperties(
            textalign="center",
        )
    )
    document.styles.addElement(title_cell)
    styles["title_cell"] = title_cell

    title = Style(
        name="Title",
        family="paragraph",
    )
    title.addElement(
        TextProperties(
            fontsize="16pt",
            fontweight="bold",
        )
    )
    title.addElement(
        ParagraphProperties(
            marginbottom="0.1cm",
        )
    )
    document.styles.addElement(title)
    styles["title"] = title

    subtitle = Style(
        name="Subtitle",
        family="paragraph",
    )
    subtitle.addElement(
        TextProperties(
            fontsize="10pt",
            color="#666666",
        )
    )
    subtitle.addElement(
        ParagraphProperties(
            marginbottom="0.35cm",
        )
    )
    document.styles.addElement(subtitle)
    styles["subtitle"] = subtitle

    space_title_cell = Style(
        name="SpaceTitleCell",
        family="table-cell",
    )
    space_title_cell.addElement(
        TableCellProperties(
            backgroundcolor="#666666",
            padding="0.16cm",
            border="0.02cm solid #555555",
            verticalalign="middle",
        )
    )
    space_title_cell.addElement(
        ParagraphProperties(
            textalign="center",
        )
    )
    space_title_cell.addElement(
        TextProperties(
            color="#ffffff",
            fontsize="12pt",
            fontweight="bold",
        )
    )
    document.styles.addElement(space_title_cell)
    styles["space_title_cell"] = space_title_cell

    centered_header_cell = Style(
        name="CenteredHeaderCell",
        family="table-cell",
    )
    centered_header_cell.addElement(
        TableCellProperties(
            backgroundcolor="#333333",
            padding="0.12cm",
            border="0.02cm solid #666666",
        )
    )
    centered_header_cell.addElement(
        ParagraphProperties(
            textalign="center",
        )
    )
    document.styles.addElement(centered_header_cell)
    styles["centered_header_cell"] = centered_header_cell

    header_text = Style(
        name="HeaderText",
        family="paragraph",
    )
    header_text.addElement(
        TextProperties(
            color="#ffffff",
            fontweight="bold",
        )
    )
    document.styles.addElement(header_text)
    styles["header_text"] = header_text

    normal_text = Style(
        name="NormalText",
        family="paragraph",
    )
    normal_text.addElement(
        TextProperties(
            color="#000000",
            fontsize="9pt",
        )
    )
    document.styles.addElement(normal_text)
    styles["normal_text"] = normal_text

    warning_text = Style(
        name="WarningText",
        family="paragraph",
    )
    warning_text.addElement(
        TextProperties(
            color="#b00020",
            fontsize="9pt",
            fontweight="bold",
        )
    )
    document.styles.addElement(warning_text)
    styles["warning_text"] = warning_text

    centered_text = Style(
        name="CenteredText",
        family="paragraph",
    )
    centered_text.addElement(
        TextProperties(
            color="#000000",
            fontsize="9pt",
        )
    )
    document.styles.addElement(centered_text)
    styles["centered_text"] = centered_text

    centered_warning_text = Style(
        name="CenteredWarningText",
        family="paragraph",
    )
    centered_warning_text.addElement(
        TextProperties(
            color="#b00020",
            fontsize="9pt",
            fontweight="bold",
        )
    )
    document.styles.addElement(centered_warning_text)
    styles["centered_warning_text"] = centered_warning_text

    grade_text = Style(
        name="GradeText",
        family="paragraph",
    )
    grade_text.addElement(
        TextProperties(
            color="#000000",
            fontsize="9pt",
        )
    )
    document.styles.addElement(grade_text)
    styles["grade_text"] = grade_text

    grade_warning_text = Style(
        name="GradeWarningText",
        family="paragraph",
    )
    grade_warning_text.addElement(
        TextProperties(
            color="#b00020",
            fontsize="9pt",
            fontweight="bold",
        )
    )
    document.styles.addElement(grade_warning_text)
    styles["grade_warning_text"] = grade_warning_text

    return styles

def create_route_cell_styles(
    document: Any,
) -> dict[str, dict[str, Any]]:
    styles: dict[str, dict[str, Any]] = {
        "normal": {},
        "centered": {},
        "grade": {},
    }

    for grade in GRADE_COLORS:
        background_color = grade_background(grade)

        normal_style = Style(
            name=f"RouteCell_{grade}",
            family="table-cell",
        )
        normal_style.addElement(
            TableCellProperties(
                backgroundcolor=background_color,
                padding="0.10cm",
                border="0.02cm solid #cccccc",
                verticalalign="middle",
            )
        )
        document.automaticstyles.addElement(normal_style)
        styles["normal"][grade] = normal_style

        centered_style = Style(
            name=f"CenteredRouteCell_{grade}",
            family="table-cell",
        )
        centered_style.addElement(
            TableCellProperties(
                backgroundcolor=background_color,
                padding="0.10cm",
                border="0.02cm solid #cccccc",
                verticalalign="middle",
            )
        )
        centered_style.addElement(
            ParagraphProperties(
                textalign="center",
            )
        )
        document.automaticstyles.addElement(centered_style)
        styles["centered"][grade] = centered_style

        grade_style = Style(
            name=f"GradeRouteCell_{grade}",
            family="table-cell",
        )
        grade_style.addElement(
            TableCellProperties(
                backgroundcolor=background_color,
                padding="0.10cm",
                paddingleft="0.50cm",
                border="0.02cm solid #cccccc",
                verticalalign="middle",
            )
        )
        document.automaticstyles.addElement(grade_style)
        styles["grade"][grade] = grade_style

    for style_kind in styles:
        fallback_style = Style(
            name=f"{style_kind.title()}RouteCell_fallback",
            family="table-cell",
        )
        fallback_style.addElement(
            TableCellProperties(
                backgroundcolor="#ffffff",
                padding="0.10cm",
                border="0.02cm solid #cccccc",
                verticalalign="middle",
            )
        )

        if style_kind == "centered":
            fallback_style.addElement(
                ParagraphProperties(
                    textalign="center",
                )
            )

        if style_kind == "grade":
            fallback_style.addElement(
                TableCellProperties(
                    paddingleft="0.50cm",
                )
            )

        document.automaticstyles.addElement(fallback_style)
        styles[style_kind]["fallback"] = fallback_style

    return styles


def add_title_rows(
    table: Any,
    styles: dict[str, Any],
    title: str,
    generated_at: date,
    route_count: int,
) -> None:
    title_row = TableRow()
    title_cell = TableCell(
        stylename=styles["title_cell"],
        numbercolumnsspanned=str(len(HEADERS)),
    )
    add_text(
        title_cell,
        title,
        styles["title"],
    )
    title_row.addElement(title_cell)
    table.addElement(title_row)

    subtitle_row = TableRow()
    subtitle_cell = TableCell(
        numbercolumnsspanned=str(len(HEADERS)),
    )
    add_text(
        subtitle_cell,
        (
            f"Générée le {generated_at.strftime('%d/%m/%Y')} "
            f"· {route_count} voies"
        ),
        styles["subtitle"],
    )
    subtitle_row.addElement(subtitle_cell)
    table.addElement(subtitle_row)

def add_space_title_row(
    table: Any,
    styles: dict[str, Any],
    space: str,
) -> None:
    row = TableRow()

    cell = TableCell(
        stylename=styles["space_title_cell"],
        numbercolumnsspanned=str(len(HEADERS)),
    )
    add_text(
        cell,
        format_space(space),
    )

    row.addElement(cell)
    table.addElement(row)


def add_header_row(
    table: Any,
    styles: dict[str, Any],
) -> None:
    row = TableRow()

    for header in HEADERS:
        cell = TableCell(
            stylename=styles["centered_header_cell"],
        )
        add_text(
            cell,
            header,
            styles["header_text"],
        )
        row.addElement(cell)

    table.addElement(row)


def add_route_row(
    table: Any,
    styles: dict[str, Any],
    route_cell_styles: dict[str, dict[str, Any]],
    route: Route,
    status: str,
    generated_at: date,
) -> None:
    row = TableRow()

    normalized_grade = normalize_grade(route.grade)

    normal_cell_style = route_cell_styles["normal"].get(
        normalized_grade,
        route_cell_styles["normal"]["fallback"],
    )

    centered_cell_style = route_cell_styles["centered"].get(
        normalized_grade,
        route_cell_styles["centered"]["fallback"],
    )

    grade_cell_style = route_cell_styles["grade"].get(
        normalized_grade,
        route_cell_styles["grade"]["fallback"],
    )

    warning = is_rotation_warning(
        route,
        generated_at,
    )

    text_style = (
        styles["warning_text"]
        if warning
        else styles["normal_text"]
    )

    centered_style = (
        styles["centered_warning_text"]
        if warning
        else styles["centered_text"]
    )

    grade_style = (
        styles["grade_warning_text"]
        if warning
        else styles["grade_text"]
    )

    leading_values = (
        (
            format_sector(route.display_sector),
            centered_cell_style,
            centered_style,
        ),
        (
            route.grade,
            grade_cell_style,
            grade_style,
        ),
    )

    for (
        value,
        cell_style,
        paragraph_style,
    ) in leading_values:
        cell = TableCell(
            stylename=cell_style,
        )
        add_text(
            cell,
            value,
            paragraph_style,
        )
        row.addElement(cell)

    hold_colors = route.hold_colors or ("#ffffff",)

    hold_cell = TableCell(
        stylename=centered_cell_style,
    )

    hold_text = " ".join(
        "■"
        for _ in hold_colors
    )

    add_text(
        hold_cell,
        hold_text,
        centered_style,
    )
    row.addElement(hold_cell)

    opened_at = route.opened_at.strftime("%d/%m/%Y")
    warning_symbol = "⚠" if warning else ""

    remaining_values = (
        (
            route.name,
            normal_cell_style,
            text_style,
        ),
        (
            ", ".join(route.openers) or "?",
            normal_cell_style,
            text_style,
        ),
        (
            opened_at,
            centered_cell_style,
            centered_style,
        ),
        (
            warning_symbol,
            centered_cell_style,
            centered_style,
        ),
        (
            status,
            centered_cell_style,
            centered_style,
        ),
    )

    for (
        value,
        cell_style,
        paragraph_style,
    ) in remaining_values:
        cell = TableCell(
            stylename=cell_style,
        )
        add_text(
            cell,
            value,
            paragraph_style,
        )
        row.addElement(cell)

    table.addElement(row)


def add_columns(
    document: Any,
    table: Any,
) -> None:
    for index, width in enumerate(COLUMN_WIDTHS):
        style = Style(
            name=f"Column_{index}",
            family="table-column",
        )
        style.addElement(
            TableColumnProperties(
                columnwidth=width,
            )
        )
        document.automaticstyles.addElement(style)

        table.addElement(
            TableColumn(
                stylename=style,
            )
        )


def add_todo_sheet(
    document: Any,
    styles: dict[str, Any],
    route_cell_styles: dict[str, dict[str, Any]],
    sheet_name: str,
    title: str,
    routes: list[Route],
    route_ascents: dict[int, list[Ascent]],
    generated_at: date,
    mode: str,
) -> None:
    table = Table(name=sheet_name)

    add_columns(
        document,
        table,
    )

    sorted_routes = sorted(
        routes,
        key=route_sort_key,
    )

    add_title_rows(
        table=table,
        styles=styles,
        title=title,
        generated_at=generated_at,
        route_count=len(sorted_routes),
    )

    current_space: str | None = None

    for route in sorted_routes:
        if route.space != current_space:
            current_space = route.space

            add_space_title_row(
                table=table,
                styles=styles,
                space=current_space,
            )

            add_header_row(
                table=table,
                styles=styles,
            )

        history = build_route_history(
            route_ascents.get(route.id, [])
        )

        if mode == "top_rope":
            status = (
                "projet"
                if history.worked
                else ""
            )
        elif history.has_top_rope:
            status = "moul' ok"
        elif history.has_unknown_roping:
            status = "?"
        elif history.worked:
            status = "projet"
        else:
            status = ""

        add_route_row(
            table=table,
            styles=styles,
            route_cell_styles=route_cell_styles,
            route=route,
            status=status,
            generated_at=generated_at,
        )

    document.spreadsheet.addElement(table)


def export_todo_ods(
    output_path: Path,
    top_rope_routes: list[Route],
    lead_routes: list[Route],
    route_ascents: dict[int, list[Ascent]],
    generated_at: date,
) -> None:
    document = OpenDocumentSpreadsheet()

    styles = create_styles(document)
    route_cell_styles = create_route_cell_styles(
        document
    )

    add_todo_sheet(
        document=document,
        styles=styles,
        route_cell_styles=route_cell_styles,
        sheet_name="Moulinette",
        title="TO-DO MOULINETTE",
        routes=top_rope_routes,
        route_ascents=route_ascents,
        generated_at=generated_at,
        mode="top_rope",
    )

    add_todo_sheet(
        document=document,
        styles=styles,
        route_cell_styles=route_cell_styles,
        sheet_name="Tête",
        title="TO-DO TÊTE",
        routes=lead_routes,
        route_ascents=route_ascents,
        generated_at=generated_at,
        mode="lead",
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    document.save(str(output_path))