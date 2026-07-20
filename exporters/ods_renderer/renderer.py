from datetime import date
from pathlib import Path
from typing import Any

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import (
    MasterPage,
    PageLayout,
    PageLayoutProperties,
    Style,
    TableColumnProperties,
)

from odf.table import (
    Table,
    TableCell,
    TableColumn,
    TableRow,
)

from odf.text import P, Span

from todo.builder import build_route_history
from todo.models import Ascent, Route

from .colors import (
    normalize_grade,
)

from .constants import (
    HEADERS,
    COLUMN_WIDTHS,
    FIRST_PAGE_ROWS,
    CONTINUATION_PAGE_ROWS,
)
from .dismantling import get_dismantling_indicator

from .helpers import (
    format_sector,
    format_space,
    is_rotation_warning,
)

from .pagination import (
    paginate_routes,
    route_sort_key,
)

from .styles import (
    create_styles,
    create_route_cell_styles,
    create_hold_color_styles,

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

def add_hold_colors(
    cell: Any,
    hold_colors: tuple[str, ...],
    hold_color_styles: dict[str, Any],
) -> None:
    paragraph = P()

    for index, color in enumerate(hold_colors):
        normalized_color = color.casefold()

        if index > 0:
            paragraph.addText(" ")

        paragraph.addElement(
            Span(
                stylename=hold_color_styles[
                    normalized_color
                ],
                text="■",
            )
        )

    cell.addElement(paragraph)


def add_warning_dot(
    cell: Any,
    level: str,
    warning_styles: dict[str, Any],
) -> None:
    if level == "":
        cell.addElement(P())
        return

    paragraph = P()

    paragraph.addElement(
        Span(
            stylename=warning_styles[level],
            text="●",
        )
    )

    cell.addElement(paragraph)


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


def add_title_rows(
    table: Any,
    styles: dict[str, Any],
    title: str,
    user_name: str,
    generated_at: date,
    route_count: int,
    mode: str,
    top_rope_grade_min: str,
    top_rope_grade_max: str,
    lead_grade_min: str,
    lead_grade_max: str,
    page_break: bool = False,
) -> None:
    title_row = TableRow(
        stylename=(
            styles["test_row_break"]
            if page_break
            else None
        )
    )
    title_cell = TableCell(
        stylename=styles["title_cell"],
        numbercolumnsspanned=str(len(HEADERS)),
    )
    if mode == "top_rope":
        grade_min = top_rope_grade_min
        grade_max = top_rope_grade_max
    else:
        grade_min = lead_grade_min
        grade_max = lead_grade_max
    add_text(
        title_cell,
        f"{title} · {grade_min} → {grade_max} ({route_count} voies)",
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
            f"{user_name} · {generated_at.strftime('%d/%m/%Y')}"
        ),
        styles["subtitle"],
    )
    subtitle_row.addElement(subtitle_cell)
    table.addElement(subtitle_row)


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


def add_space_title_row(
    table: Any,
    styles: dict[str, Any],
    space: str,
    page_break: bool = False,
) -> None:
    row = TableRow()
    cell = TableCell(
        stylename=styles["space_title_cell"],
        numbercolumnsspanned=str(len(HEADERS)),
    )

    paragraph_style = (
        styles["space_title_text"]
    )

    add_text(
        cell,
        format_space(space),
        paragraph_style,
    )
    row.addElement(cell)
    table.addElement(row)


def add_route_row(
    table: Any,
    styles: dict[str, Any],
    route_cell_styles: dict[str, dict[str, Any]],
    hold_color_styles: dict[str, Any],
    all_routes_in_space: list[Route],
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

    critical_cell_style = route_cell_styles["critical"].get(
        normalized_grade,
        route_cell_styles["critical"]["fallback"],
    )

    centered_cell_style = route_cell_styles["centered"].get(
        normalized_grade,
        route_cell_styles["centered"]["fallback"],
    )

    centered_critical_cell_style = route_cell_styles[
        "centered_critical"
    ].get(
        normalized_grade,
        route_cell_styles["centered_critical"]["fallback"],
    )

    grade_cell_style = route_cell_styles["grade"].get(
        normalized_grade,
        route_cell_styles["grade"]["fallback"],
    )

    warning_level = get_dismantling_indicator(
        route=route,
        all_routes_in_space=all_routes_in_space,
        today=generated_at,
    )

    is_critical = warning_level == "critical"
    is_warning = warning_level == "warning"

    checkbox_cell = TableCell(
        stylename=centered_cell_style,
    )
    add_text(
        checkbox_cell,
        "☐",
    )
    row.addElement(checkbox_cell)

    leading_values = (
        (
            format_sector(route.display_sector),
            centered_cell_style,
        ),
        (
            route.grade,
            grade_cell_style,
        ),
    )

    for (
        value,
        cell_style,
    ) in leading_values:
        cell = TableCell(
            stylename=cell_style,
        )
        add_text(
            cell,
            value,
        )
        row.addElement(cell)

    hold_colors = route.hold_colors or (
        "#ffffff",
    )

    hold_cell = TableCell(
        stylename=centered_cell_style,
    )

    add_hold_colors(
        cell=hold_cell,
        hold_colors=hold_colors,
        hold_color_styles=hold_color_styles,
    )

    row.addElement(hold_cell)

    opened_at = route.opened_at.strftime("%d/%m/%Y")

    warning_cell_style = route_cell_styles["warning"].get(
        normalized_grade,
        route_cell_styles["warning"]["fallback"],
    )

    centered_warning_cell_style = route_cell_styles[
        "centered_warning"
    ].get(
        normalized_grade,
        route_cell_styles["centered_warning"]["fallback"],
    )

    if is_critical:
        name_style = critical_cell_style
        symbol_style = centered_critical_cell_style
    elif is_warning:
        name_style = warning_cell_style
        symbol_style = centered_warning_cell_style
    else:
        name_style = normal_cell_style
        symbol_style = centered_cell_style

    remaining_values = (
        (
            route.name,
            name_style,
        ),
        (
            ", ".join(route.openers) or "?",
            normal_cell_style,
        ),
        (
            opened_at,
            centered_cell_style,
        ),
        (
            "●" if warning_level else "",
            symbol_style,
        ),
        (
            status,
            centered_cell_style,
        ),
    )

    for (
        value,
        cell_style,
    ) in remaining_values:
        cell = TableCell(
            stylename=cell_style,
        )
        add_text(
            cell,
            value,
        )
        row.addElement(cell)

    table.addElement(row)
   

def create_page_layout(
    document: Any,
) -> Any:
    page_layout = PageLayout(
        name="TodoPageLayout",
    )

    page_layout.addElement(
        PageLayoutProperties(
            pagewidth="29.7cm",
            pageheight="21cm",
            printorientation="landscape",
            margintop="1cm",
            marginbottom="1cm",
            marginleft="1cm",
            marginright="1cm",
        )
    )

    document.automaticstyles.addElement(
        page_layout
    )

    master_page = MasterPage(
        name="TodoMasterPage",
        pagelayoutname=page_layout,
    )

    document.masterstyles.addElement(
        master_page
    )

    return master_page

def add_todo_sheet(
    document: Any,
    styles: dict[str, Any],
    route_cell_styles: dict[str, dict[str, Any]],
    hold_color_styles: dict[str, Any],
    master_page: Any,
    sheet_name: str,
    title: str,
    all_routes: list[Route],
    routes: list[Route],
    route_ascents: dict[int, list[Ascent]],
    user_name: str,
    generated_at: date,
    mode: str,
    top_rope_grade_min: str,
    top_rope_grade_max: str,
    lead_grade_min: str,
    lead_grade_max: str,
    space_order: dict[str, int],
) -> None:
    table_style = Style(
        name=f"{sheet_name}Table",
        family="table",
        masterpagename=master_page,
    )

    document.automaticstyles.addElement(
        table_style
    )

    table = Table(
        name=sheet_name,
        stylename=table_style,
    )

    add_columns(
        document,
        table,
    )

    routes_by_space: dict[str, list[Route]] = {}

    for route in routes:
        routes_by_space.setdefault(
            route.space,
            [],
        ).append(route)
    
    all_routes_by_space: dict[str, list[Route]] = {}

    for route in all_routes:
        all_routes_by_space.setdefault(
            route.space,
            [],
        ).append(route)

    first_page = True

    for space in space_order:
        space_routes = sorted(
            routes_by_space.get(space, []),
            key=route_sort_key,
        )

        if not space_routes:
            continue

        route_pages = paginate_routes(
            routes=space_routes,
            first_page_rows=FIRST_PAGE_ROWS,
            continuation_rows=CONTINUATION_PAGE_ROWS,
        )

        add_title_rows(
            table=table,
            styles=styles,
            title=title,
            user_name=user_name,
            generated_at=generated_at,
            route_count=len(space_routes),
            mode=mode,
            top_rope_grade_min=top_rope_grade_min,
            top_rope_grade_max=top_rope_grade_max,
            lead_grade_min=lead_grade_min,
            lead_grade_max=lead_grade_max,
            page_break=not first_page
        )

        for route_page in route_pages:

            add_space_title_row(
                table=table,
                styles=styles,
                space=space,
            )

            add_header_row(
                table=table,
                styles=styles,
            )

            for route in route_page:
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
                    hold_color_styles=hold_color_styles,
                    all_routes_in_space=all_routes_by_space[route.space],
                    route=route,
                    status=status,
                    generated_at=generated_at,
                )
            
            first_page = False

        document.spreadsheet.addElement(table)

def export_todo_ods(
    output_path: Path,
    all_routes: list[Route],
    top_rope_routes: list[Route],
    lead_routes: list[Route],
    route_ascents: dict[int, list[Ascent]],
    user_name: str,
    generated_at: date,
    top_rope_grade_min: str,
    top_rope_grade_max: str,
    lead_grade_min: str,
    lead_grade_max: str,
    space_order: dict[str, int],
) -> None:
    document = OpenDocumentSpreadsheet()

    master_page = create_page_layout(
        document
    )

    styles = create_styles(document)
    route_cell_styles = create_route_cell_styles(
        document
    )

    hold_color_styles = create_hold_color_styles(
        document=document,
        routes=top_rope_routes + lead_routes,
    )

    add_todo_sheet(
        document=document,
        styles=styles,
        route_cell_styles=route_cell_styles,
        hold_color_styles=hold_color_styles,
        master_page=master_page,
        sheet_name="Moulinette",
        title="MOULINETTE",
        all_routes=all_routes,
        routes=top_rope_routes,
        route_ascents=route_ascents,
        user_name=user_name,
        generated_at=generated_at,
        mode="top_rope",
        top_rope_grade_min=top_rope_grade_min,
        top_rope_grade_max=top_rope_grade_max,
        lead_grade_min=lead_grade_min,
        lead_grade_max=lead_grade_max,
        space_order=space_order,
    )

    add_todo_sheet(
        document=document,
        styles=styles,
        route_cell_styles=route_cell_styles,
        hold_color_styles=hold_color_styles,
        master_page=master_page,
        sheet_name="Tête",
        title="TÊTE",
        all_routes=all_routes,
        routes=lead_routes,
        route_ascents=route_ascents,
        user_name=user_name,
        generated_at=generated_at,
        mode="lead",
        top_rope_grade_min=top_rope_grade_min,
        top_rope_grade_max=top_rope_grade_max,
        lead_grade_min=lead_grade_min,
        lead_grade_max=lead_grade_max,
        space_order=space_order,
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    document.save(str(output_path))