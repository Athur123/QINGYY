#!/usr/bin/env python3
"""Convert Markdown spec to PDF using reportlab with Chinese font support."""

import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Chinese font
pdfmetrics.registerFont(TTFont('STHeiti', '/System/Library/Fonts/STHeiti Light.ttc'))

MD_PATH = '/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/2026-04-25-settlement-entity-financial-attribution-design.md'
PDF_PATH = '/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/2026-04-25-settlement-entity-financial-attribution-design.pdf'

FONT_MAIN = 'STHeiti'
FONT_SIZE_BASE = 10
LINE_HEIGHT = 1.4

# Colors
COLOR_PRIMARY = HexColor('#2563EB')
COLOR_TEXT = HexColor('#1E293B')
COLOR_TEXT_SECONDARY = HexColor('#64748B')
COLOR_BORDER = HexColor('#E2E8F0')
COLOR_BG_LIGHT = HexColor('#F8FAFC')
COLOR_BG_TABLE_HEADER = HexColor('#F1F5F9')
COLOR_BG_BLOCKQUOTE = HexColor('#EFF6FF')
COLOR_TAG_BG = HexColor('#FEF3C7')
COLOR_TAG_TEXT = HexColor('#D97706')
COLOR_CHECK_GREEN = HexColor('#16A34A')
COLOR_CHECK_YELLOW = HexColor('#CA8A04')


def parse_markdown(text):
    """Parse markdown into a list of (type, content) tokens."""
    lines = text.split('\n')
    tokens = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Blockquote
        if line.startswith('> '):
            bq_lines = []
            while i < len(lines) and lines[i].startswith('> '):
                bq_lines.append(lines[i][2:])
                i += 1
            tokens.append(('blockquote', '\n'.join(bq_lines)))
            continue

        # Horizontal rule
        if re.match(r'^-{3,}$', line.strip()):
            tokens.append(('hr', ''))
            i += 1
            continue

        # Heading
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            tokens.append(('heading', (level, m.group(2))))
            i += 1
            continue

        # Table
        if '|' in line and i + 1 < len(lines) and re.match(r'^[\s|:-]+$', lines[i + 1]):
            # Parse header
            headers = [h.strip() for h in line.strip('|').split('|')]
            i += 2  # skip header and separator
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                row = [c.strip() for c in lines[i].strip('|').split('|')]
                rows.append(row)
                i += 1
            tokens.append(('table', (headers, rows)))
            continue

        # Code block
        if line.startswith('```'):
            lang = line[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            tokens.append(('code_block', '\n'.join(code_lines)))
            continue

        # Inline code
        # Bullet list
        if re.match(r'^[-*]\s+', line):
            items = []
            while i < len(lines) and re.match(r'^[-*]\s+', lines[i]):
                items.append(re.sub(r'^[-*]\s+', '', lines[i]))
                i += 1
            tokens.append(('list', items))
            continue

        # Numbered list
        if re.match(r'^\d+\.\s+', line):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                items.append(re.sub(r'^\d+\.\s+', '', lines[i]))
                i += 1
            tokens.append(('numbered_list', items))
            continue

        # Empty line
        if not line.strip():
            i += 1
            continue

        # Paragraph
        tokens.append(('paragraph', line))
        i += 1

    return tokens


def inline_format(text):
    """Apply inline formatting to text."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<font face="Courier">' + r'\1</font>', text)
    # Emoji-style tags
    text = re.sub(r'🔸', r'<font color="#D97706">🔸</font>', text)
    return text


def create_styles():
    """Create paragraph styles."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'Title_Custom',
        parent=styles['Title'],
        fontName=FONT_MAIN,
        fontSize=18,
        textColor=COLOR_TEXT,
        spaceAfter=6 * mm,
        spaceBefore=0,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName=FONT_MAIN,
        fontSize=14,
        textColor=COLOR_PRIMARY,
        spaceBefore=12 * mm,
        spaceAfter=6 * mm,
        borderWidth=0,
        borderColor=COLOR_PRIMARY,
        borderPadding=0,
    ))

    styles.add(ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName=FONT_MAIN,
        fontSize=12,
        textColor=COLOR_TEXT,
        spaceBefore=8 * mm,
        spaceAfter=4 * mm,
    ))

    styles.add(ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontName=FONT_MAIN,
        fontSize=11,
        textColor=COLOR_TEXT,
        spaceBefore=6 * mm,
        spaceAfter=3 * mm,
    ))

    styles.add(ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName=FONT_MAIN,
        fontSize=FONT_SIZE_BASE,
        textColor=COLOR_TEXT,
        leading=FONT_SIZE_BASE * LINE_HEIGHT,
        spaceBefore=2 * mm,
        spaceAfter=2 * mm,
    ))

    styles.add(ParagraphStyle(
        'Blockquote',
        parent=styles['Normal'],
        fontName=FONT_MAIN,
        fontSize=FONT_SIZE_BASE - 1,
        textColor=COLOR_TEXT_SECONDARY,
        leading=(FONT_SIZE_BASE - 1) * LINE_HEIGHT,
        leftIndent=10 * mm,
        rightIndent=5 * mm,
        spaceBefore=4 * mm,
        spaceAfter=4 * mm,
        borderWidth=0,
        borderColor=COLOR_PRIMARY,
        borderPadding=3 * mm,
    ))

    styles.add(ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        leftIndent=8 * mm,
        rightIndent=5 * mm,
        spaceBefore=4 * mm,
        spaceAfter=4 * mm,
        textColor=HexColor('#334155'),
        backColor=COLOR_BG_LIGHT,
        borderWidth=0.5,
        borderColor=COLOR_BORDER,
        borderPadding=4 * mm,
    ))

    styles.add(ParagraphStyle(
        'ListItem',
        parent=styles['Normal'],
        fontName=FONT_MAIN,
        fontSize=FONT_SIZE_BASE,
        textColor=COLOR_TEXT,
        leading=FONT_SIZE_BASE * LINE_HEIGHT,
        leftIndent=12 * mm,
        firstLineIndent=-6 * mm,
        spaceBefore=1 * mm,
        spaceAfter=1 * mm,
    ))

    return styles


def build_table(headers, rows, styles):
    """Build a table element."""
    col_count = len(headers)
    # Calculate column widths
    page_width = A4[0] - 4 * cm  # usable width
    col_width = page_width / col_count
    col_widths = [col_width] * col_count

    # Header row
    header_data = [Paragraph(inline_format(h), styles['Body_Custom']) for h in headers]
    table_data = [header_data]

    for row in rows:
        row_data = []
        for cell in row:
            cell_text = inline_format(cell)
            row_data.append(Paragraph(cell_text, styles['Body_Custom']))
        table_data.append(row_data)

    t = Table(table_data, colWidths=col_widths)

    # Style
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_BG_TABLE_HEADER),
        ('FONTNAME', (0, 0), (-1, -1), FONT_MAIN),
        ('FONTSIZE', (0, 0), (-1, -1), FONT_SIZE_BASE - 1),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]

    # Highlight tag cells
    for row_idx, row in enumerate(rows):
        for col_idx, cell in enumerate(row):
            if '🔸' in cell:
                style_cmds.append(
                    ('BACKGROUND', (col_idx, row_idx + 1), (col_idx, row_idx + 1), COLOR_TAG_BG)
                )

    t.setStyle(TableStyle(style_cmds))
    return t


def build_pdf():
    """Main function to build the PDF."""
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    tokens = parse_markdown(md_text)
    styles = create_styles()

    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title='结算主体减员权限与费用管理设计',
        author='青阳云HRO系统',
    )

    story = []

    for token_type, content in tokens:
        if token_type == 'heading':
            level, text = content
            if level == 1:
                style_key = 'Heading1_Custom'
            elif level == 2:
                style_key = 'Heading2_Custom'
            elif level == 3:
                style_key = 'Heading3_Custom'
            else:
                style_key = 'Body_Custom'
            story.append(Paragraph(inline_format(text), styles[style_key]))

        elif token_type == 'paragraph':
            story.append(Paragraph(inline_format(content), styles['Body_Custom']))

        elif token_type == 'blockquote':
            # Render as a styled paragraph
            formatted = inline_format(content)
            p = Paragraph(formatted, styles['Blockquote'])
            story.append(p)

        elif token_type == 'code_block':
            story.append(Paragraph(content.replace('\n', '<br/>'), styles['CodeBlock']))

        elif token_type == 'table':
            headers, rows = content
            story.append(Spacer(0, 3 * mm))
            table = build_table(headers, rows, styles)
            story.append(table)
            story.append(Spacer(0, 3 * mm))

        elif token_type == 'list':
            for item in content:
                bullet = '• '
                story.append(Paragraph(bullet + inline_format(item), styles['ListItem']))

        elif token_type == 'numbered_list':
            for idx, item in enumerate(content, 1):
                story.append(Paragraph(f'{idx}. {inline_format(item)}', styles['ListItem']))

        elif token_type == 'hr':
            story.append(HRFlowable(width='100%', thickness=0.5, color=COLOR_BORDER, spaceBefore=3*mm, spaceAfter=3*mm))

    doc.build(story)
    print(f'PDF created: {PDF_PATH}')


if __name__ == '__main__':
    build_pdf()
