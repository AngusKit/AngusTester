#!/usr/bin/env python3
"""Generate a professional year-end summary PPT with 19 slides."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Color palette ──────────────────────────────────────────────
DARK_BLUE   = RGBColor(0x1B, 0x2A, 0x4A)
MID_BLUE    = RGBColor(0x2C, 0x3E, 0x6B)
LIGHT_BLUE  = RGBColor(0x3A, 0x7C, 0xBD)
ORANGE      = RGBColor(0xE8, 0x6C, 0x00)
WARM_ORANGE = RGBColor(0xFF, 0x8C, 0x21)
GREEN       = RGBColor(0x27, 0xAE, 0x60)
DARK_GREEN  = RGBColor(0x1E, 0x8A, 0x4C)
RED         = RGBColor(0xE7, 0x4C, 0x3C)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY  = RGBColor(0xF5, 0xF5, 0xF5)
MED_GRAY    = RGBColor(0x95, 0xA5, 0xA6)
DARK_GRAY   = RGBColor(0x34, 0x49, 0x5E)
GOLD        = RGBColor(0xF3, 0x9C, 0x12)
BLACK       = RGBColor(0x00, 0x00, 0x00)
ACCENT_BLUE = RGBColor(0x29, 0x80, 0xB9)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

W = prs.slide_width
H = prs.slide_height

# ── Helper functions ───────────────────────────────────────────

def add_blank_slide():
    layout = prs.slide_layouts[6]  # blank
    return prs.slides.add_slide(layout)


def fill_background(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_gradient_rect(slide, left, top, width, height, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_textbox(slide, left, top, width, height, text="", font_size=18,
                font_color=WHITE, bold=False, alignment=PP_ALIGN.LEFT,
                font_name="Microsoft YaHei"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = font_color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_paragraph(text_frame, text, font_size=16, font_color=WHITE,
                  bold=False, alignment=PP_ALIGN.LEFT, space_before=Pt(6),
                  space_after=Pt(4), font_name="Microsoft YaHei"):
    p = text_frame.add_paragraph()
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = font_color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    p.space_before = space_before
    p.space_after = space_after
    return p


def add_accent_line(slide, left, top, width, color=WARM_ORANGE, height=Pt(4)):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_circle_number(slide, left, top, size, number, bg_color=WARM_ORANGE):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].text = str(number)
    tf.paragraphs[0].font.size = Pt(14)
    tf.paragraphs[0].font.color.rgb = WHITE
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.name = "Microsoft YaHei"
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return shape


def add_card(slide, left, top, width, height, color=RGBColor(0x22, 0x36, 0x5A)):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def build_table(slide, rows_data, left, top, width, col_widths, header_color=LIGHT_BLUE, row_height=Inches(0.45)):
    rows = len(rows_data)
    cols = len(rows_data[0])
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, row_height * rows)
    table = table_shape.table
    for i, w in enumerate(col_widths):
        table.columns[i].width = w
    for r_idx, row in enumerate(rows_data):
        for c_idx, cell_text in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = cell_text
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(12)
                paragraph.font.name = "Microsoft YaHei"
                paragraph.alignment = PP_ALIGN.CENTER
                if r_idx == 0:
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = WHITE
                else:
                    paragraph.font.color.rgb = WHITE
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_color
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0x1F, 0x30, 0x52) if r_idx % 2 == 1 else RGBColor(0x26, 0x3B, 0x5E)
    return table_shape


def add_sidebar(slide, color=WARM_ORANGE, width=Inches(0.12)):
    add_gradient_rect(slide, Inches(0), Inches(0), width, H, color)


def add_page_number(slide, num, total=19):
    add_textbox(slide, W - Inches(1.2), H - Inches(0.5), Inches(1), Inches(0.4),
                f"{num} / {total}", font_size=10, font_color=MED_GRAY,
                alignment=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════
# Slide 1 — Cover
# ══════════════════════════════════════════════════════════════
def slide_01_cover():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_gradient_rect(slide, Inches(0), Inches(0), W, Inches(0.08), WARM_ORANGE)
    add_gradient_rect(slide, Inches(0), H - Inches(0.08), W, Inches(0.08), WARM_ORANGE)

    add_accent_line(slide, Inches(4.5), Inches(2.4), Inches(4.3), WARM_ORANGE, Pt(5))

    add_textbox(slide, Inches(2), Inches(2.6), Inches(9.3), Inches(1.2),
                "2024年度工作总结与2025展望", font_size=42, font_color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(2), Inches(4.0), Inches(9.3), Inches(0.6),
                "XX科技有限公司", font_size=22, font_color=LIGHT_BLUE,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(2), Inches(4.8), Inches(9.3), Inches(0.5),
                "汇报人：XXX", font_size=16, font_color=MED_GRAY,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(2), Inches(5.3), Inches(9.3), Inches(0.5),
                "2025年X月X日", font_size=14, font_color=MED_GRAY,
                alignment=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════
# Slide 2 — Agenda
# ══════════════════════════════════════════════════════════════
def slide_02_agenda():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(8), Inches(0.8),
                "本次会议主题", font_size=32, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(1.15), Inches(2.5))

    add_textbox(slide, Inches(0.8), Inches(1.5), Inches(11), Inches(0.6),
                "回顾2024 · 正视问题 · 拥抱变化 · 布局未来",
                font_size=18, font_color=WARM_ORANGE, bold=True)

    items = [
        "年度自我复盘与反思",
        "AI浪潮下的行业变革",
        "客户战略转型：从toB到toC",
        "出海战略：美元支付全球化销售",
        "新产品与新方向规划",
        "7月融资计划与资金使用规划",
    ]
    y_start = Inches(2.4)
    for i, item in enumerate(items):
        add_circle_number(slide, Inches(1.2), y_start + Inches(i * 0.75), Inches(0.45), i + 1)
        add_textbox(slide, Inches(2.0), y_start + Inches(i * 0.75) - Pt(2), Inches(9), Inches(0.5),
                    item, font_size=18, font_color=WHITE)

    add_page_number(slide, 2)


# ══════════════════════════════════════════════════════════════
# Slide 3 — Self-criticism overview
# ══════════════════════════════════════════════════════════════
def slide_03_self_criticism():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, RED)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(10), Inches(0.8),
                "直面问题，才能解决问题", font_size=32, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(1.15), Inches(3), RED)

    card = add_card(slide, Inches(1.5), Inches(2.2), Inches(10), Inches(3),
                    RGBColor(0x2A, 0x1A, 0x1A))
    tf = card.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].space_before = Pt(20)
    p = tf.paragraphs[0]
    p.text = ""
    add_paragraph(tf, "2024年是艰难的一年，", font_size=24, font_color=WHITE, bold=True,
                  space_before=Pt(30))
    add_paragraph(tf, "我们在业绩、产品、项目三个维度均未达预期。", font_size=22, font_color=WHITE)
    add_paragraph(tf, "", font_size=14)
    add_paragraph(tf, "作为公司负责人，我负主要责任。", font_size=22, font_color=RED, bold=True,
                  space_before=Pt(20))

    labels = ["业绩", "产品", "项目"]
    colors = [RED, ORANGE, GOLD]
    for i, (label, clr) in enumerate(zip(labels, colors)):
        x = Inches(2.5) + Inches(i * 3)
        shape = add_card(slide, x, Inches(5.7), Inches(2.2), Inches(1.0), clr)
        tf2 = shape.text_frame
        tf2.paragraphs[0].text = label
        tf2.paragraphs[0].font.size = Pt(20)
        tf2.paragraphs[0].font.color.rgb = WHITE
        tf2.paragraphs[0].font.bold = True
        tf2.paragraphs[0].font.name = "Microsoft YaHei"
        tf2.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf2.vertical_anchor = MSO_ANCHOR.MIDDLE

    add_page_number(slide, 3)


# ══════════════════════════════════════════════════════════════
# Slide 4 — Revenue review
# ══════════════════════════════════════════════════════════════
def slide_04_revenue():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, RED)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(10), Inches(0.8),
                "业绩：距目标差距明显", font_size=32, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(1.15), Inches(3), RED)

    table_data = [
        ["指标", "目标", "实际", "差距"],
        ["年度营收", "200万", "18.8万", "-181.2万"],
    ]
    col_w = [Inches(2.5), Inches(2.5), Inches(2.5), Inches(2.5)]
    build_table(slide, table_data, Inches(1), Inches(1.6), Inches(10), col_w,
                header_color=RED, row_height=Inches(0.55))

    add_textbox(slide, Inches(1), Inches(3.0), Inches(5), Inches(0.5),
                "收入构成：", font_size=18, font_color=WARM_ORANGE, bold=True)
    txBox = add_textbox(slide, Inches(1), Inches(3.5), Inches(5), Inches(1.2), font_size=16, font_color=WHITE)
    tf = txBox.text_frame
    tf.paragraphs[0].text = "· 基础收入：1万"
    tf.paragraphs[0].font.size = Pt(16)
    tf.paragraphs[0].font.color.rgb = WHITE
    tf.paragraphs[0].font.name = "Microsoft YaHei"
    add_paragraph(tf, "· 项目收入：17.8万", font_size=16, font_color=WHITE)

    add_textbox(slide, Inches(7), Inches(3.0), Inches(5.5), Inches(0.5),
                "反思：", font_size=18, font_color=RED, bold=True)
    txBox2 = add_textbox(slide, Inches(7), Inches(3.5), Inches(5.5), Inches(3), font_size=16, font_color=WHITE)
    tf2 = txBox2.text_frame
    tf2.paragraphs[0].text = "✗  200万营收门槛未达到"
    tf2.paragraphs[0].font.size = Pt(16)
    tf2.paragraphs[0].font.color.rgb = RED
    tf2.paragraphs[0].font.name = "Microsoft YaHei"
    add_paragraph(tf2, "✗  商业模式尚未跑通，营收结构单一", font_size=16, font_color=RED)
    add_paragraph(tf2, "✗  市场拓展力度不足，客户转化率低", font_size=16, font_color=RED)

    big = add_textbox(slide, Inches(1.5), Inches(5.4), Inches(10), Inches(1.5),
                      "", font_size=14, font_color=MED_GRAY)
    tf3 = big.text_frame
    add_paragraph(tf3, "18.8万 vs 200万目标 —— 仅完成 9.4%",
                  font_size=28, font_color=RED, bold=True, alignment=PP_ALIGN.CENTER)

    add_page_number(slide, 4)


# ══════════════════════════════════════════════════════════════
# Slide 5 — Product issues
# ══════════════════════════════════════════════════════════════
def slide_05_product():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, RED)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(10), Inches(0.8),
                "产品：推倒重来的阵痛", font_size=32, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(1.15), Inches(3), RED)

    points = [
        "产品方向经历重大调整",
        "前期研发投入的工作基本需要重新来过",
        "时间成本与资金成本双重损失",
    ]
    for i, pt in enumerate(points):
        add_card(slide, Inches(1), Inches(1.8 + i * 0.9), Inches(10.5), Inches(0.7),
                 RGBColor(0x2A, 0x1A, 0x1A))
        add_textbox(slide, Inches(1.4), Inches(1.85 + i * 0.9), Inches(10), Inches(0.6),
                    f"▸  {pt}", font_size=18, font_color=WARM_ORANGE)

    add_textbox(slide, Inches(1), Inches(4.8), Inches(10), Inches(0.5),
                "根因分析", font_size=22, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(1), Inches(5.3), Inches(1.8), RED)

    causes = [
        "前期产品定位不够精准",
        "市场需求验证不充分",
        "技术路线选择需要迭代优化",
    ]
    for i, c in enumerate(causes):
        add_textbox(slide, Inches(1.4), Inches(5.5 + i * 0.55), Inches(10), Inches(0.5),
                    f"•  {c}", font_size=16, font_color=WHITE)

    add_page_number(slide, 5)


# ══════════════════════════════════════════════════════════════
# Slide 6 — Project review
# ══════════════════════════════════════════════════════════════
def slide_06_projects():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, RED)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(10), Inches(0.8),
                "项目：4个项目参与，0个签约", font_size=32, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(1.15), Inches(3), RED)

    table_data = [
        ["项目", "阶段", "结果"],
        ["项目A", "深度参与", "✗ 未签约"],
        ["项目B", "方案提交", "✗ 未签约"],
        ["项目C", "商务洽谈", "✗ 未签约"],
        ["项目D", "技术对接", "✗ 未签约"],
    ]
    col_w = [Inches(3), Inches(3.5), Inches(3.5)]
    build_table(slide, table_data, Inches(1), Inches(1.6), Inches(10), col_w,
                header_color=RED, row_height=Inches(0.5))

    add_textbox(slide, Inches(1), Inches(4.5), Inches(10), Inches(0.5),
                "反思", font_size=22, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(1), Inches(5.0), Inches(1.2), RED)

    reflections = [
        "签约转化率为0，需重新审视销售策略",
        "toB项目签约周期长、决策链复杂、回款慢",
        "过度依赖toB大客户模式，抗风险能力弱",
    ]
    for i, r in enumerate(reflections):
        add_textbox(slide, Inches(1.4), Inches(5.2 + i * 0.55), Inches(10), Inches(0.5),
                    f"•  {r}", font_size=16, font_color=WHITE)

    add_page_number(slide, 6)


# ══════════════════════════════════════════════════════════════
# Slide 7 — AI transition page
# ══════════════════════════════════════════════════════════════
def slide_07_ai_transition():
    slide = add_blank_slide()
    fill_background(slide, MID_BLUE)
    add_gradient_rect(slide, Inches(0), Inches(0), W, Inches(0.08), WARM_ORANGE)
    add_gradient_rect(slide, Inches(0), H - Inches(0.08), W, Inches(0.08), WARM_ORANGE)

    add_textbox(slide, Inches(1), Inches(2.3), Inches(11.3), Inches(1.2),
                "顺势而为 · 拥抱AI浪潮", font_size=44, font_color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

    add_accent_line(slide, Inches(5), Inches(3.7), Inches(3.3), WARM_ORANGE, Pt(5))

    add_textbox(slide, Inches(2), Inches(4.2), Inches(9.3), Inches(1),
                "\"当风来的时候，不要建墙，要建风车。\"",
                font_size=22, font_color=GOLD, alignment=PP_ALIGN.CENTER)

    add_page_number(slide, 7)


# ══════════════════════════════════════════════════════════════
# Slide 8 — AI changes
# ══════════════════════════════════════════════════════════════
def slide_08_ai_changes():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, ORANGE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(10), Inches(0.8),
                "AI正在重塑软件测试行业", font_size=32, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(1.15), Inches(3), ORANGE)

    cards_info = [
        ("技术进步", ORANGE, [
            "AI驱动的自动化测试、智能缺陷检测",
            "测试用例自动生成、代码审查智能化",
        ]),
        ("效率提升", WARM_ORANGE, [
            "传统需要10人团队的项目，现在3-5人即可",
            "测试周期大幅缩短，交付速度倍增",
        ]),
        ("一人公司的可能性", GOLD, [
            "AI赋能下，小团队可交付中大型项目",
            "降低人力成本，提升利润空间",
            "这是我们\"小而美\"公司的最大机遇",
        ]),
    ]
    for i, (title, clr, bullets) in enumerate(cards_info):
        x = Inches(0.8) + Inches(i * 4.1)
        card = add_card(slide, x, Inches(1.8), Inches(3.7), Inches(5.0), RGBColor(0x1F, 0x30, 0x52))
        add_gradient_rect(slide, x, Inches(1.8), Inches(3.7), Inches(0.7), clr)
        add_textbox(slide, x + Inches(0.2), Inches(1.85), Inches(3.3), Inches(0.6),
                    title, font_size=20, font_color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
        for j, b in enumerate(bullets):
            add_textbox(slide, x + Inches(0.3), Inches(2.8 + j * 0.7), Inches(3.2), Inches(0.7),
                        f"• {b}", font_size=14, font_color=WHITE)

    add_page_number(slide, 8)


# ══════════════════════════════════════════════════════════════
# Slide 9 — AI opportunities
# ══════════════════════════════════════════════════════════════
def slide_09_ai_opportunities():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, ORANGE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(10), Inches(0.8),
                "危机 = 危险 + 机会", font_size=32, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(1.15), Inches(3), ORANGE)

    add_textbox(slide, Inches(1), Inches(1.6), Inches(5.5), Inches(0.5),
                "行业机遇", font_size=22, font_color=WARM_ORANGE, bold=True)
    industry = [
        "传统测试外包市场正在被颠覆",
        "→ 智能测试服务需求激增",
        "企业对\"AI+测试\"解决方案买单意愿增强",
        "全球中小企业和个人开发者",
        "对轻量级测试工具需求爆发",
    ]
    for i, t in enumerate(industry):
        add_textbox(slide, Inches(1.3), Inches(2.2 + i * 0.5), Inches(5), Inches(0.5),
                    f"• {t}" if not t.startswith("\u2192") and not t.startswith("→") else f"  {t}", font_size=14, font_color=WHITE)

    add_textbox(slide, Inches(7), Inches(1.6), Inches(5.5), Inches(0.5),
                "我们的机遇", font_size=22, font_color=WARM_ORANGE, bold=True)
    ours = [
        "船小好掉头，快速转型AI测试服务",
        "用AI工具武装团队，以小博大",
        "从服务国内toB客户",
        "→ 产品化出海服务全球toC用户",
    ]
    for i, t in enumerate(ours):
        clr = GOLD if "产品化出海" in t else WHITE
        bld = "产品化出海" in t
        add_textbox(slide, Inches(7.3), Inches(2.2 + i * 0.5), Inches(5), Inches(0.5),
                    f"• {t}" if not t.startswith("→") else f"  {t}", font_size=14, font_color=clr, bold=bld)

    add_page_number(slide, 9)


# ══════════════════════════════════════════════════════════════
# Slide 10 — toB to toC strategy
# ══════════════════════════════════════════════════════════════
def slide_10_tob_toc():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, ORANGE)

    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.7),
                "战略转型：toB → toC为重心", font_size=30, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(0.95), Inches(3), ORANGE)

    card_b = add_card(slide, Inches(0.5), Inches(1.3), Inches(5.8), Inches(3.2), RGBColor(0x3A, 0x1A, 0x1A))
    add_textbox(slide, Inches(0.8), Inches(1.35), Inches(5), Inches(0.45),
                "toB模式的痛点（过去）", font_size=18, font_color=RED, bold=True)
    tob_items = [
        "销售周期长（3-6个月甚至更久）",
        "决策链复杂（多层审批、招投标）",
        "回款周期慢，现金流压力大",
        "定制化需求多，难以规模化",
        "4个项目0签约，充分验证了困境",
    ]
    for i, t in enumerate(tob_items):
        add_textbox(slide, Inches(1.0), Inches(1.9 + i * 0.48), Inches(5), Inches(0.45),
                    f"✗  {t}", font_size=13, font_color=RGBColor(0xE8, 0x99, 0x99))

    card_c = add_card(slide, Inches(6.8), Inches(1.3), Inches(5.8), Inches(3.2), RGBColor(0x1A, 0x3A, 0x1A))
    add_textbox(slide, Inches(7.1), Inches(1.35), Inches(5), Inches(0.45),
                "toC模式的优势（未来）", font_size=18, font_color=GREEN, bold=True)
    toc_items = [
        "用户自主注册、自主付费，无需商务谈判",
        "标准化产品，边际成本趋近于零",
        "付费决策快（个人/小团队决策）",
        "现金流健康，按月/按年订阅",
        "用户基数大，增长天花板更高",
    ]
    for i, t in enumerate(toc_items):
        add_textbox(slide, Inches(7.3), Inches(1.9 + i * 0.48), Inches(5), Inches(0.45),
                    f"✓  {t}", font_size=13, font_color=RGBColor(0x99, 0xE8, 0x99))

    add_textbox(slide, Inches(5.8), Inches(2.4), Inches(1.5), Inches(0.8),
                "→", font_size=48, font_color=WARM_ORANGE, bold=True, alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(0.8), Inches(4.8), Inches(5), Inches(0.5),
                "目标客户画像", font_size=20, font_color=WARM_ORANGE, bold=True)
    cust_data = [
        ["维度", "描述"],
        ["用户类型", "独立开发者、自由职业者、小型创业团队"],
        ["地区", "全球市场（重点：北美、欧洲、东南亚）"],
        ["需求", "轻量级、即开即用的AI测试工具/平台"],
        ["付费能力", "$9-$99/月 订阅制"],
    ]
    col_w = [Inches(2), Inches(9)]
    build_table(slide, cust_data, Inches(0.8), Inches(5.3), Inches(11), col_w,
                header_color=ORANGE, row_height=Inches(0.38))

    add_page_number(slide, 10)


# ══════════════════════════════════════════════════════════════
# Slide 11 — Going global
# ══════════════════════════════════════════════════════════════
def slide_11_global():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, ORANGE)

    add_textbox(slide, Inches(0.8), Inches(0.25), Inches(10), Inches(0.6),
                "出海 · 赚美元 · 全球化", font_size=30, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(0.82), Inches(3), ORANGE)

    add_textbox(slide, Inches(0.8), Inches(1.1), Inches(6), Inches(0.4),
                "为什么要出海？", font_size=18, font_color=WARM_ORANGE, bold=True)
    why_items = [
        "全球开发者超3000万，测试工具市场持续增长",
        "美元定价，汇率优势（1美元≈7.2元人民币）",
        "海外用户付费意愿强，SaaS订阅模式成熟",
        "国内卷价格，海外卷价值",
    ]
    for i, t in enumerate(why_items):
        add_textbox(slide, Inches(1.1), Inches(1.55 + i * 0.4), Inches(5.5), Inches(0.4),
                    f"• {t}", font_size=12, font_color=WHITE)

    add_textbox(slide, Inches(7), Inches(1.1), Inches(6), Inches(0.4),
                "美元支付体系搭建", font_size=18, font_color=WARM_ORANGE, bold=True)
    pay_data = [
        ["模块", "方案"],
        ["支付渠道", "Stripe / Paddle / LemonSqueezy"],
        ["定价策略", "美元计价，Free/Pro/Enterprise三档"],
        ["收款主体", "海外公司 或 Payoneer等"],
        ["合规", "税务合规（VAT/GST自动处理）"],
    ]
    col_w2 = [Inches(1.8), Inches(4)]
    build_table(slide, pay_data, Inches(7), Inches(1.5), Inches(5.8), col_w2,
                header_color=ORANGE, row_height=Inches(0.38))

    add_textbox(slide, Inches(0.8), Inches(3.7), Inches(10), Inches(0.4),
                "出海销售策略", font_size=18, font_color=WARM_ORANGE, bold=True)
    strategies = [
        ("Product Hunt / Hacker News", "首发获取种子用户"),
        ("SEO + 内容营销", "英文博客、YouTube教程、技术文档"),
        ("社媒运营", "Twitter/X、Reddit、LinkedIn、Discord"),
        ("Affiliate联盟营销", "让用户帮你卖"),
        ("Free增值模式", "免费版引流 → 付费版转化"),
    ]
    for i, (s1, s2) in enumerate(strategies):
        x = Inches(0.8) + Inches((i % 3) * 4.1)
        y = Inches(4.3) + Inches((i // 3) * 1.3)
        card = add_card(slide, x, y, Inches(3.7), Inches(1.1), RGBColor(0x1F, 0x30, 0x52))
        add_textbox(slide, x + Inches(0.2), y + Inches(0.05), Inches(3.3), Inches(0.45),
                    s1, font_size=14, font_color=WARM_ORANGE, bold=True)
        add_textbox(slide, x + Inches(0.2), y + Inches(0.5), Inches(3.3), Inches(0.45),
                    s2, font_size=12, font_color=WHITE)

    add_page_number(slide, 11)


# ══════════════════════════════════════════════════════════════
# Slide 12 — New product & direction
# ══════════════════════════════════════════════════════════════
def slide_12_new_product():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, ORANGE)

    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.7),
                "2025：破局之年", font_size=32, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(0.95), Inches(2.5), ORANGE)

    add_textbox(slide, Inches(0.8), Inches(1.3), Inches(5), Inches(0.5),
                "新产品规划", font_size=20, font_color=WARM_ORANGE, bold=True)
    products = [
        "AI智能测试平台（自动化测试+AI分析）",
        "— 全球SaaS版本",
        "面向个人开发者和小团队的轻量级质量保障工具",
        "支持多语言、多框架，开箱即用",
    ]
    for i, p in enumerate(products):
        add_textbox(slide, Inches(1.1), Inches(1.8 + i * 0.45), Inches(5.5), Inches(0.45),
                    f"▸ {p}", font_size=14, font_color=WHITE)

    add_textbox(slide, Inches(0.8), Inches(3.8), Inches(5), Inches(0.5),
                "新方向（三大转变）", font_size=20, font_color=WARM_ORANGE, bold=True)
    trans_data = [
        ["从（过去）", "到（未来）"],
        ["人力驱动", "AI+人力混合模式"],
        ["toB项目制", "toC产品订阅制"],
        ["国内市场", "全球市场·美元收入"],
    ]
    col_w = [Inches(3), Inches(3)]
    build_table(slide, trans_data, Inches(0.8), Inches(4.3), Inches(6), col_w,
                header_color=ORANGE, row_height=Inches(0.45))

    add_textbox(slide, Inches(7.5), Inches(1.3), Inches(5), Inches(0.5),
                "关键目标", font_size=20, font_color=WARM_ORANGE, bold=True)
    targets = [
        "完成新产品MVP并上线（中英文双版本）",
        "搭建美元支付出海体系",
        "年底实现MRR $10,000+",
        "建立可复制、可规模化的SaaS商业模式",
    ]
    for i, t in enumerate(targets):
        card = add_card(slide, Inches(7.5), Inches(1.9 + i * 1.05), Inches(5), Inches(0.85),
                        RGBColor(0x1F, 0x30, 0x52))
        add_textbox(slide, Inches(7.8), Inches(2.0 + i * 1.05), Inches(4.5), Inches(0.7),
                    f"✓  {t}", font_size=15, font_color=GREEN)

    add_page_number(slide, 12)


# ══════════════════════════════════════════════════════════════
# Slide 13 — Fundraising overview
# ══════════════════════════════════════════════════════════════
def slide_13_fundraising():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, GREEN)

    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.7),
                "融资计划：为规模化增长蓄力", font_size=30, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(0.95), Inches(3), GREEN)

    add_textbox(slide, Inches(0.8), Inches(1.3), Inches(5), Inches(0.5),
                "启动时间：2025年7月", font_size=20, font_color=GREEN, bold=True)
    add_textbox(slide, Inches(0.8), Inches(1.8), Inches(6), Inches(0.4),
                "为什么是7月？", font_size=16, font_color=WARM_ORANGE, bold=True)
    why_july = [
        "Q1-Q2：完成产品MVP、验证市场需求、跑通商业模式",
        "7月：带着产品+数据+用户去融资，而非PPT融资",
        "用前6个月的成绩证明方向可行",
    ]
    for i, t in enumerate(why_july):
        add_textbox(slide, Inches(1.1), Inches(2.2 + i * 0.4), Inches(5.5), Inches(0.4),
                    f"• {t}", font_size=13, font_color=WHITE)

    add_textbox(slide, Inches(7), Inches(1.3), Inches(5.5), Inches(0.5),
                "融资目标", font_size=20, font_color=GREEN, bold=True)
    fund_data = [
        ["项目", "内容"],
        ["融资轮次", "天使轮 / Pre-A"],
        ["融资金额", "200-500万人民币"],
        ["资金用途", "团队扩充 + 推广运营"],
        ["出让股比", "10%-20%"],
    ]
    col_w = [Inches(2), Inches(3.5)]
    build_table(slide, fund_data, Inches(7), Inches(1.8), Inches(5.5), col_w,
                header_color=GREEN, row_height=Inches(0.42))

    add_textbox(slide, Inches(0.8), Inches(4.0), Inches(11), Inches(0.5),
                "融资前的关键里程碑（融资\"入场券\"）", font_size=20, font_color=GREEN, bold=True)
    milestones = [
        ("产品上线并稳定运行", GREEN),
        ("付费用户≥100人", GREEN),
        ("MRR≥$2,000（证明营收能力）", GREEN),
        ("用户月增长率≥20%（证明增长潜力）", GREEN),
    ]
    for i, (m, clr) in enumerate(milestones):
        x = Inches(0.8) + Inches((i % 2) * 6)
        y = Inches(4.7) + Inches((i // 2) * 1.1)
        card = add_card(slide, x, y, Inches(5.5), Inches(0.85), RGBColor(0x1A, 0x30, 0x1A))
        add_textbox(slide, x + Inches(0.3), y + Inches(0.1), Inches(5), Inches(0.65),
                    f"✓  {m}", font_size=15, font_color=clr)

    add_page_number(slide, 13)


# ══════════════════════════════════════════════════════════════
# Slide 14 — Team expansion
# ══════════════════════════════════════════════════════════════
def slide_14_team():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, GREEN)

    add_textbox(slide, Inches(0.8), Inches(0.2), Inches(10), Inches(0.6),
                "团队扩充计划：精兵强将，10人以内", font_size=28, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(0.78), Inches(3), GREEN)

    add_textbox(slide, Inches(0.8), Inches(0.95), Inches(11), Inches(0.4),
                "核心原则：AI时代不堆人头，每个人都是多面手，10人团队打出50人的战斗力",
                font_size=13, font_color=WARM_ORANGE, bold=True)

    team_data = [
        ["序号", "岗位", "人数", "月薪预估", "职责"],
        ["1", "创始人/CEO", "1", "—", "战略、产品、融资"],
        ["2", "全栈工程师", "2", "2-3万/人", "产品研发、AI功能开发"],
        ["3", "AI算法工程师", "1", "2.5-4万", "AI模型训练、测试智能化"],
        ["4", "前端工程师", "1", "1.5-2.5万", "用户界面、产品体验"],
        ["5", "海外增长/运营", "2", "1.5-2.5万/人", "SEO、内容营销、社媒运营"],
        ["6", "客户成功", "1", "1-1.5万", "用户支持、留存、反馈收集"],
        ["7", "设计师（兼职）", "1", "0.8-1.2万", "UI/UX、品牌视觉"],
        ["", "合计", "9-10人", "", ""],
    ]
    col_w = [Inches(0.8), Inches(2.2), Inches(1.2), Inches(2), Inches(4)]
    build_table(slide, team_data, Inches(0.5), Inches(1.4), Inches(10.2), col_w,
                header_color=GREEN, row_height=Inches(0.37))

    add_textbox(slide, Inches(0.8), Inches(4.9), Inches(5), Inches(0.4),
                "团队年度人力成本预估", font_size=16, font_color=GREEN, bold=True)
    cost_data = [
        ["项目", "金额"],
        ["月度人力成本", "约15-22万/月"],
        ["年度人力成本", "约180-260万/年"],
        ["融资后6个月成本", "约90-130万"],
    ]
    col_w2 = [Inches(2.5), Inches(2.5)]
    build_table(slide, cost_data, Inches(0.8), Inches(5.3), Inches(5), col_w2,
                header_color=GREEN, row_height=Inches(0.38))

    add_textbox(slide, Inches(7), Inches(4.9), Inches(5.5), Inches(0.4),
                "招聘策略", font_size=16, font_color=GREEN, bold=True)
    hire_strategies = [
        "优先远程办公，降低办公成本，扩大人才池",
        "技术岗优先招有AI工具使用经验的人",
        "海外运营岗可招聘海外华人或本地化人才",
        "前期核心岗位可给期权，降低现金压力",
    ]
    for i, s in enumerate(hire_strategies):
        add_textbox(slide, Inches(7.2), Inches(5.4 + i * 0.45), Inches(5.3), Inches(0.4),
                    f"• {s}", font_size=13, font_color=WHITE)

    add_page_number(slide, 14)


# ══════════════════════════════════════════════════════════════
# Slide 15 — Marketing budget
# ══════════════════════════════════════════════════════════════
def slide_15_marketing():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, GREEN)

    add_textbox(slide, Inches(0.8), Inches(0.2), Inches(10), Inches(0.6),
                "推广运营预算：精准投放，高效增长", font_size=28, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(0.78), Inches(3), GREEN)

    mkt_data = [
        ["类别", "项目", "预算(万元)", "说明"],
        ["付费投放", "Google Ads", "20-30", "关键词广告，精准获客"],
        ["付费投放", "Twitter/X Ads", "5-10", "开发者社区精准投放"],
        ["付费投放", "Reddit Ads", "3-5", "技术社区定向推广"],
        ["内容营销", "SEO+博客", "5-8", "英文技术文章、教程产出"],
        ["内容营销", "YouTube视频", "3-5", "产品教程、技术分享"],
        ["社区运营", "Discord/社群", "2-3", "用户社区建设与维护"],
        ["社区运营", "开源社区", "2-3", "GitHub开源项目引流"],
        ["品牌曝光", "Product Hunt", "1-2", "首发活动策划与推广"],
        ["品牌曝光", "技术大会/赞助", "3-5", "海外开发者大会曝光"],
        ["联盟营销", "Affiliate计划", "5-8", "用户推荐返佣机制"],
        ["工具/基建", "SaaS工具订阅", "3-5", "分析、邮件、客服等工具"],
        ["工具/基建", "服务器/云服务", "8-12", "AWS/GCP 产品部署"],
        ["", "合计", "60-96万", ""],
    ]
    col_w = [Inches(1.5), Inches(2.5), Inches(1.8), Inches(4.5)]
    build_table(slide, mkt_data, Inches(0.4), Inches(1.1), Inches(10.3), col_w,
                header_color=GREEN, row_height=Inches(0.33))

    add_textbox(slide, Inches(0.8), Inches(5.8), Inches(5), Inches(0.4),
                "预期获客效果", font_size=16, font_color=GREEN, bold=True)
    effect_data = [
        ["指标", "目标"],
        ["CAC（获客成本）", "≤$15/注册用户"],
        ["注册用户", "10,000+"],
        ["付费转化率", "5%-8%"],
        ["付费用户", "500-800人"],
        ["LTV", "≥$200"],
        ["LTV/CAC", "≥3"],
    ]
    col_w3 = [Inches(2.5), Inches(2.5)]
    build_table(slide, effect_data, Inches(6.5), Inches(5.8), Inches(5), col_w3,
                header_color=GREEN, row_height=Inches(0.22))

    add_page_number(slide, 15)


# ══════════════════════════════════════════════════════════════
# Slide 16 — Fund allocation & ROI
# ══════════════════════════════════════════════════════════════
def slide_16_fund_allocation():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, GREEN)

    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.7),
                "融资资金使用总览", font_size=30, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(0.95), Inches(3), GREEN)

    add_textbox(slide, Inches(0.8), Inches(1.3), Inches(10), Inches(0.4),
                "资金分配（以融资300万为例）", font_size=18, font_color=WARM_ORANGE, bold=True)

    alloc = [
        ("团队扩充", "150万 (50%)", "9-10人团队", RGBColor(0x27, 0xAE, 0x60)),
        ("推广运营", "96万 (32%)", "全球化推广", RGBColor(0x29, 0x80, 0xB9)),
        ("储备金", "54万 (18%)", "风险储备", RGBColor(0xF3, 0x9C, 0x12)),
    ]
    for i, (label, amount, desc, clr) in enumerate(alloc):
        x = Inches(1) + Inches(i * 3.8)
        card = add_card(slide, x, Inches(1.9), Inches(3.4), Inches(2.0), clr)
        add_textbox(slide, x + Inches(0.2), Inches(2.0), Inches(3), Inches(0.45),
                    label, font_size=20, font_color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
        add_textbox(slide, x + Inches(0.2), Inches(2.5), Inches(3), Inches(0.45),
                    amount, font_size=18, font_color=WHITE, alignment=PP_ALIGN.CENTER)
        add_textbox(slide, x + Inches(0.2), Inches(3.0), Inches(3), Inches(0.45),
                    desc, font_size=14, font_color=RGBColor(0xDD, 0xDD, 0xDD), alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(0.8), Inches(4.3), Inches(10), Inches(0.5),
                "投资回报预期（融资后12个月）", font_size=18, font_color=GREEN, bold=True)
    roi_data = [
        ["时间", "MRR目标", "ARR换算", "付费用户数"],
        ["融资后3个月 (Q4 2025)", "$5,000", "$60,000", "200+"],
        ["融资后6个月 (Q1 2026)", "$15,000", "$180,000", "500+"],
        ["融资后9个月 (Q2 2026)", "$30,000", "$360,000", "1,000+"],
        ["融资后12个月 (Q3 2026)", "$50,000", "$600,000", "1,500+"],
    ]
    col_w = [Inches(3.2), Inches(2), Inches(2.2), Inches(2)]
    build_table(slide, roi_data, Inches(0.8), Inches(4.8), Inches(9.4), col_w,
                header_color=GREEN, row_height=Inches(0.42))

    add_textbox(slide, Inches(0.8), Inches(6.5), Inches(11), Inches(0.35),
                "核心承诺：融资后12个月内达到 ARR $600,000（约430万人民币）· 实现正向现金流 · 为A轮打下基础",
                font_size=14, font_color=GOLD, bold=True)

    add_page_number(slide, 16)


# ══════════════════════════════════════════════════════════════
# Slide 17 — 2025 Roadmap
# ══════════════════════════════════════════════════════════════
def slide_17_roadmap():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, ACCENT_BLUE)

    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.7),
                "2025 Roadmap · 全年关键里程碑", font_size=30, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(0.95), Inches(3), ACCENT_BLUE)

    quarters = [
        ("Q1 (1-3月)", ACCENT_BLUE, [
            "产品MVP开发 + 英文版上线",
            "搭建美元支付体系（Stripe/Paddle）",
            "种子用户获取，验证PMF",
        ]),
        ("Q2 (4-6月)", WARM_ORANGE, [
            "Product Hunt发布",
            "首批1000注册用户 / 100付费用户",
            "MRR达$2,000+",
            "准备融资材料（BP、财务模型、数据）",
        ]),
        ("Q3 (7-9月)", GREEN, [
            "7月启动融资，完成天使轮/Pre-A",
            "团队扩充至5-7人",
            "启动付费推广（Google Ads等）",
            "MRR达$5,000-$10,000",
        ]),
        ("Q4 (10-12月)", GOLD, [
            "团队扩充至9-10人",
            "MRR达$10,000-$15,000",
            "产品迭代2.0版本",
            "年终目标：ARR $120,000-$180,000",
        ]),
    ]

    for i, (q_label, clr, items) in enumerate(quarters):
        x = Inches(0.5) + Inches(i * 3.15)
        add_gradient_rect(slide, x, Inches(1.4), Inches(2.9), Inches(0.65), clr)
        add_textbox(slide, x + Inches(0.1), Inches(1.42), Inches(2.7), Inches(0.6),
                    q_label, font_size=18, font_color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
        card = add_card(slide, x, Inches(2.15), Inches(2.9), Inches(4.8),
                        RGBColor(0x1F, 0x30, 0x52))
        for j, item in enumerate(items):
            add_textbox(slide, x + Inches(0.15), Inches(2.4 + j * 0.9), Inches(2.6), Inches(0.85),
                        f"▸ {item}", font_size=13, font_color=WHITE)

    add_page_number(slide, 17)


# ══════════════════════════════════════════════════════════════
# Slide 18 — Summary & outlook
# ══════════════════════════════════════════════════════════════
def slide_18_summary():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_sidebar(slide, WARM_ORANGE)

    add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.7),
                "总结与展望", font_size=32, font_color=WHITE, bold=True)
    add_accent_line(slide, Inches(0.8), Inches(0.95), Inches(2.5), WARM_ORANGE)

    add_textbox(slide, Inches(0.8), Inches(1.3), Inches(5.5), Inches(0.5),
                "2024 → 教训与成长", font_size=20, font_color=RED, bold=True)
    add_textbox(slide, Inches(6.5), Inches(1.3), Inches(6), Inches(0.5),
                "2025 → 转型·出海·融资·突破", font_size=20, font_color=GREEN, bold=True)

    checks = [
        "正视问题，不回避、不粉饰",
        "拥抱AI，把技术变革转化为产品竞争力",
        "从toB转向toC，拥抱规模化增长",
        "出海赚美元，用全球市场打开收入天花板",
        "7月融资，用资本加速团队和增长",
        "小步快跑，快速验证、快速迭代",
    ]
    for i, c in enumerate(checks):
        col = 0 if i < 3 else 1
        row = i if i < 3 else i - 3
        x = Inches(1.0) if col == 0 else Inches(6.7)
        add_textbox(slide, x, Inches(1.9 + row * 0.55), Inches(5.5), Inches(0.5),
                    f"✓  {c}", font_size=15, font_color=WHITE)

    add_card(slide, Inches(1), Inches(4.2), Inches(5), Inches(1.2), RGBColor(0x3A, 0x1A, 0x1A))
    add_textbox(slide, Inches(1.3), Inches(4.3), Inches(4.5), Inches(0.45),
                "2024年营收", font_size=14, font_color=MED_GRAY)
    add_textbox(slide, Inches(1.3), Inches(4.7), Inches(4.5), Inches(0.55),
                "18.8万人民币", font_size=26, font_color=RED, bold=True)

    add_textbox(slide, Inches(5.8), Inches(4.65), Inches(1), Inches(0.5),
                "→", font_size=36, font_color=WARM_ORANGE, bold=True, alignment=PP_ALIGN.CENTER)

    add_card(slide, Inches(6.8), Inches(4.2), Inches(5.5), Inches(1.2), RGBColor(0x1A, 0x3A, 0x1A))
    add_textbox(slide, Inches(7.1), Inches(4.3), Inches(5), Inches(0.45),
                "2025年目标", font_size=14, font_color=MED_GRAY)
    add_textbox(slide, Inches(7.1), Inches(4.7), Inches(5), Inches(0.55),
                "ARR $120,000-$180,000（≈86-130万）", font_size=22, font_color=GREEN, bold=True)

    quotes = [
        "\"不出海，就出局。\"",
        "\"先用6个月证明自己，再用资本放大自己。\"",
        "在AI时代，10个人可以改变一个行业。",
    ]
    for i, q in enumerate(quotes):
        add_textbox(slide, Inches(1), Inches(5.8 + i * 0.45), Inches(11), Inches(0.4),
                    q, font_size=16, font_color=GOLD, alignment=PP_ALIGN.CENTER)

    add_page_number(slide, 18)


# ══════════════════════════════════════════════════════════════
# Slide 19 — Thank you
# ══════════════════════════════════════════════════════════════
def slide_19_thanks():
    slide = add_blank_slide()
    fill_background(slide, DARK_BLUE)
    add_gradient_rect(slide, Inches(0), Inches(0), W, Inches(0.08), WARM_ORANGE)
    add_gradient_rect(slide, Inches(0), H - Inches(0.08), W, Inches(0.08), WARM_ORANGE)

    add_textbox(slide, Inches(2), Inches(2.2), Inches(9.3), Inches(1.2),
                "感谢聆听", font_size=48, font_color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

    add_accent_line(slide, Inches(5), Inches(3.6), Inches(3.3), WARM_ORANGE, Pt(5))

    add_textbox(slide, Inches(2), Inches(4.0), Inches(9.3), Inches(0.8),
                "期待与团队共同迎接2025的挑战与机遇",
                font_size=20, font_color=LIGHT_BLUE, alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(2), Inches(4.9), Inches(9.3), Inches(0.8),
                "Let's Go Global!", font_size=28, font_color=GOLD, bold=True,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(2), Inches(5.8), Inches(9.3), Inches(0.5),
                "联系方式 / 公司Logo", font_size=14, font_color=MED_GRAY,
                alignment=PP_ALIGN.CENTER)


# ── Build all slides ──────────────────────────────────────────
slide_01_cover()
slide_02_agenda()
slide_03_self_criticism()
slide_04_revenue()
slide_05_product()
slide_06_projects()
slide_07_ai_transition()
slide_08_ai_changes()
slide_09_ai_opportunities()
slide_10_tob_toc()
slide_11_global()
slide_12_new_product()
slide_13_fundraising()
slide_14_team()
slide_15_marketing()
slide_16_fund_allocation()
slide_17_roadmap()
slide_18_summary()
slide_19_thanks()

output_path = "2024年度总结与2025展望.pptx"
prs.save(output_path)
print(f"PPT saved to: {output_path}")
print(f"Total slides: {len(prs.slides)}")
