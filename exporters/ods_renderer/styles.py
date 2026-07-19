from __future__ import annotations

from typing import Any

from odf.style import (
    ParagraphProperties,
    Style,
    TableCellProperties,
    TextProperties,
)

from .colors import (
    grade_background,
)

from .constants import (
    GRADE_COLORS,
)

from todo.models import Route

from odf.element import Element

def create_styles(
    document: Any,
) -> dict[str, Any]:
    styles: dict[str, Any] = {}

    #
    # Cellules des titres
    #

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

    #
    # Paragraphes
    #

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
            fontsize="9pt",
            color="#000000",
        )
    )
    document.styles.addElement(normal_text)
    styles["normal_text"] = normal_text

    centered_text = Style(
        name="CenteredText",
        family="paragraph",
    )
    centered_text.addElement(
        ParagraphProperties(
            textalign="center",
        )
    )
    centered_text.addElement(
        TextProperties(
            fontsize="9pt",
            color="#000000",
        )
    )
    document.styles.addElement(centered_text)
    styles["centered_text"] = centered_text

    grade_text = Style(
        name="GradeText",
        family="paragraph",
    )
    grade_text.addElement(
        ParagraphProperties(
            textalign="center",
        )
    )
    grade_text.addElement(
        TextProperties(
            fontsize="9pt",
            color="#000000",
        )
    )
    document.styles.addElement(grade_text)
    styles["grade_text"] = grade_text

    checkbox_text = Style(
        name="CheckboxText",
        family="paragraph",
    )
    checkbox_text.addElement(
        ParagraphProperties(
            textalign="center",
        )
    )
    checkbox_text.addElement(
        TextProperties(
            fontsize="12pt",
        )
    )
    document.styles.addElement(checkbox_text)
    styles["checkbox_text"] = checkbox_text

    warning_text = Style(
        name="WarningText",
        family="paragraph",
    )
    warning_text.addElement(
        TextProperties(
            fontsize="9pt",
            color="#b00020",
            fontweight="bold",
        )
    )
    document.styles.addElement(warning_text)
    styles["warning_text"] = warning_text

    centered_warning_text = Style(
        name="CenteredWarningText",
        family="paragraph",
    )
    centered_warning_text.addElement(
        ParagraphProperties(
            textalign="center",
        )
    )
    centered_warning_text.addElement(
        TextProperties(
            fontsize="9pt",
            color="#b00020",
            fontweight="bold",
        )
    )
    document.styles.addElement(centered_warning_text)
    styles["centered_warning_text"] = centered_warning_text

    space_title_text = Style(
        name="SpaceTitleText",
        family="paragraph",
    )
    space_title_text.addElement(
        ParagraphProperties(
            textalign="center",
        )
    )
    space_title_text.addElement(
        TextProperties(
            fontsize="12pt",
            color="#ffffff",
            fontweight="bold",
        )
    )
    document.styles.addElement(space_title_text)
    styles["space_title_text"] = space_title_text

    page_break_space_title = Style(
        name="PageBreakSpaceTitle",
        family="paragraph",
    )
    page_break_space_title.addElement(
        ParagraphProperties(
            breakbefore="page",
            textalign="center",
        )
    )
    page_break_space_title.addElement(
        TextProperties(
            fontsize="12pt",
            color="#ffffff",
            fontweight="bold",
        )
    )
    document.styles.addElement(page_break_space_title)
    styles["page_break_space_title"] = page_break_space_title

    styles["test_row_break"] = test_row_style(document)

    return styles

def create_route_cell_styles(
    document: Any,
) -> dict[str, dict[str, Any]]:
    styles: dict[str, dict[str, Any]] = {
        "normal": {},
        "warning": {},
        "yellow": {},
        "centered": {},
        "centered_warning": {},
        "centered_yellow": {},
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

        warning_style = Style(
            name=f"RouteCellWarning_{grade}",
            family="table-cell",
        )
        warning_style.addElement(
            TableCellProperties(
                backgroundcolor=background_color,
                padding="0.10cm",
                border="0.02cm solid #cccccc",
                verticalalign="middle",
            )
        )
        warning_style.addElement(
            TextProperties(
                color="#b00020",
                fontweight="bold",
            )
        )
        document.automaticstyles.addElement(warning_style)
        styles["warning"][grade] = warning_style

        yellow_style = Style(
            name=f"RouteCellYellow_{grade}",
            family="table-cell",
        )
        yellow_style.addElement(
            TableCellProperties(
                backgroundcolor=background_color,
                padding="0.10cm",
                border="0.02cm solid #cccccc",
                verticalalign="middle",
            )
        )
        yellow_style.addElement(
            TextProperties(
                color="#FFA500",
                fontweight="bold",
            )
        )
        document.automaticstyles.addElement(yellow_style)
        styles["yellow"][grade] = yellow_style


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

        centered_warning_style = Style(
            name=f"CenteredRouteCellWarning_{grade}",
            family="table-cell",
        )
        centered_warning_style.addElement(
            TableCellProperties(
                backgroundcolor=background_color,
                padding="0.10cm",
                border="0.02cm solid #cccccc",
                verticalalign="middle",
            )
        )
        centered_warning_style.addElement(
            ParagraphProperties(
                textalign="center",
            )
        )
        centered_warning_style.addElement(
            TextProperties(
                color="#b00020",
                fontweight="bold",
            )
        )
        document.automaticstyles.addElement(centered_warning_style)
        styles["centered_warning"][grade] = centered_warning_style

        centered_yellow_style = Style(
            name=f"CenteredRouteCellYellow_{grade}",
            family="table-cell",
        )
        centered_yellow_style.addElement(
            TableCellProperties(
                backgroundcolor=background_color,
                padding="0.10cm",
                border="0.02cm solid #cccccc",
                verticalalign="middle",
            )
        )
        centered_yellow_style.addElement(
            ParagraphProperties(
                textalign="center",
            )
        )
        centered_yellow_style.addElement(
            TextProperties(
                color="#FFA500",
                fontweight="bold",
            )
        )
        document.automaticstyles.addElement(centered_yellow_style)
        styles["centered_yellow"][grade] = centered_yellow_style

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

    for style_kind in (
        "normal",
        "warning",
        "yellow",
        "centered",
        "centered_warning",
        "centered_yellow",
        "grade",
    ):
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

        if style_kind in (
            "centered",
            "centered_warning",
            "centered_yellow",
        ):
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
        
        if style_kind in (
            "warning",
            "centered_warning",
        ):
            fallback_style.addElement(
                TextProperties(
                    color="#b00020",
                    fontweight="bold",
                )
            )
        elif style_kind in (
            "yellow",
            "centered_yellow",
        ):
            fallback_style.addElement(
                TextProperties(
                    color="#FFA500",
                    fontweight="bold",
                )
            )

        document.automaticstyles.addElement(fallback_style)
        styles[style_kind]["fallback"] = fallback_style

    return styles

def create_hold_color_styles(
    document: Any,
    routes: list[Route],
) -> dict[str, Any]:
    styles: dict[str, Any] = {}

    colors = sorted(
        {
            color.casefold()
            for route in routes
            for color in route.hold_colors
        }
    )

    for color in colors:
        style = Style(
            name=f"HoldColor_{color.lstrip('#')}",
            family="text",
        )

        style.addElement(
            TextProperties(
                color=color,
                fontsize="11pt",
                fontweight="bold",
            )
        )

        document.automaticstyles.addElement(style)

        styles[color] = style

    return styles

def test_row_style(document):
    from odf.style import Style

    style = Style(
        name="TestRowBreak",
        family="table-row",
    )

    props = Element(
        qname=(
            "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
            "table-row-properties",
        )
    )

    props.setAttrNS(
        "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
        "break-before",
        "page",
    )

    style.addElement(props)

    document.automaticstyles.addElement(style)

    return style