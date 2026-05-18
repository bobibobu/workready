from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape
import os


PHOTO = Path("resume_photo.jpg")
BLUE = "1F4E79"
DARK = "1F1F1F"
GRAY = "666666"


def esc(value):
    return escape(str(value), {'"': "&quot;"})


def run(text, bold=False, size=20, color=DARK):
    bold_tag = "<w:b/>" if bold else ""
    return (
        f"<w:r><w:rPr>{bold_tag}<w:color w:val=\"{color}\"/>"
        f"<w:sz w:val=\"{size}\"/><w:szCs w:val=\"{size}\"/>"
        f"<w:rFonts w:ascii=\"Calibri\" w:hAnsi=\"Calibri\" "
        f"w:eastAsia=\"Microsoft YaHei\" w:cs=\"Microsoft YaHei\"/>"
        f"</w:rPr><w:t xml:space=\"preserve\">{esc(text)}</w:t></w:r>"
    )


def para(text="", bold=False, size=20, after=70, before=0, color=DARK, align=None, left=0, hanging=0):
    align_tag = f"<w:jc w:val=\"{align}\"/>" if align else ""
    ind = f"<w:ind w:left=\"{left}\" w:hanging=\"{hanging}\"/>" if left or hanging else ""
    return (
        f"<w:p><w:pPr><w:spacing w:before=\"{before}\" w:after=\"{after}\" "
        f"w:line=\"280\" w:lineRule=\"auto\"/>{align_tag}{ind}</w:pPr>"
        f"{run(text, bold, size, color)}</w:p>"
    )


def bullet(text):
    return para("• " + text, size=19, after=42, left=360, hanging=180)


def section(title):
    return (
        f"<w:p><w:pPr><w:spacing w:before=\"110\" w:after=\"56\"/>"
        f"<w:pBdr><w:bottom w:val=\"single\" w:sz=\"8\" w:space=\"4\" "
        f"w:color=\"{BLUE}\"/></w:pBdr></w:pPr>{run(title, True, 26, '000000')}</w:p>"
    )


def table_row(cells, widths, bold=None, sizes=None, after=30):
    bold = bold or [False] * len(cells)
    sizes = sizes or [20] * len(cells)
    out = "<w:tr>"
    for text, width, is_bold, size in zip(cells, widths, bold, sizes):
        out += (
            f"<w:tc><w:tcPr><w:tcW w:w=\"{width}\" w:type=\"dxa\"/>"
            "<w:tcBorders><w:top w:val=\"nil\"/><w:left w:val=\"nil\"/>"
            "<w:bottom w:val=\"nil\"/><w:right w:val=\"nil\"/></w:tcBorders>"
            f"</w:tcPr>{para(text, is_bold, size, after)}</w:tc>"
        )
    return out + "</w:tr>"


def two_col(left, right="", bold_left=False, bold_right=False, left_width=6200, right_width=2500):
    return (
        "<w:tbl><w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders><w:top w:val=\"nil\"/><w:left w:val=\"nil\"/>"
        "<w:bottom w:val=\"nil\"/><w:right w:val=\"nil\"/>"
        "<w:insideH w:val=\"nil\"/><w:insideV w:val=\"nil\"/></w:tblBorders>"
        "</w:tblPr>"
        + table_row([left, right], [left_width, right_width], [bold_left, bold_right], [21, 20], 20)
        + "</w:tbl>"
    )


def header(target):
    photo = ""
    if PHOTO.exists():
        photo = (
            "<w:p><w:r><w:drawing><wp:inline "
            "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
            "distT=\"0\" distB=\"0\" distL=\"0\" distR=\"0\">"
            "<wp:extent cx=\"760000\" cy=\"1012000\"/><wp:docPr id=\"1\" name=\"photo\"/>"
            "<a:graphic xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\">"
            "<a:graphicData uri=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">"
            "<pic:pic xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">"
            "<pic:nvPicPr><pic:cNvPr id=\"0\" name=\"resume_photo.jpg\"/><pic:cNvPicPr/></pic:nvPicPr>"
            "<pic:blipFill><a:blip r:embed=\"rIdPhoto\" "
            "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\"/>"
            "<a:stretch><a:fillRect/></a:stretch></pic:blipFill>"
            "<pic:spPr><a:xfrm><a:off x=\"0\" y=\"0\"/>"
            "<a:ext cx=\"760000\" cy=\"1012000\"/></a:xfrm>"
            "<a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom></pic:spPr>"
            "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>"
        )
    left = (
        para("于艳波", True, 36, 20)
        + para(target, True, 22, 46, color=BLUE)
        + para("电话：182-4806-1241    邮箱：3272871858@qq.com    城市：上海 / 呼和浩特", size=19, after=35, color=GRAY)
        + para("本科 | 软件工程 | 内蒙古大学 | 英语 CET-6", size=19, after=15, color=GRAY)
    )
    return (
        "<w:tbl><w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders><w:top w:val=\"nil\"/><w:left w:val=\"nil\"/>"
        "<w:bottom w:val=\"nil\"/><w:right w:val=\"nil\"/>"
        "<w:insideH w:val=\"nil\"/><w:insideV w:val=\"nil\"/></w:tblBorders>"
        "</w:tblPr><w:tr>"
        "<w:tc><w:tcPr><w:tcW w:w=\"7900\" w:type=\"dxa\"/></w:tcPr>"
        f"{left}</w:tc><w:tc><w:tcPr><w:tcW w:w=\"950\" w:type=\"dxa\"/></w:tcPr>{photo}</w:tc>"
        "</w:tr></w:tbl>"
    )


def experience(company, date, title, location, bullets, projects):
    out = section("工作经历")
    out += two_col(company, date, True, False)
    out += para(f"{title} | {location}", size=20, after=42, color=GRAY)
    for item in bullets:
        out += bullet(item)
    for project in projects:
        out += project_block(*project, compact=True)
    return out


def project_block(name, date, role, stack, bullets, compact=False):
    out = two_col(name, date, True, False)
    out += para(f"{role} | 技术栈：{stack}", size=19, after=40, color=GRAY)
    for item in bullets:
        out += bullet(item)
    if not compact:
        out += para("", after=40)
    return out


def education():
    return (
        section("教育背景")
        + two_col("内蒙古大学 | 软件工程 | 本科", "2020.09 - 2024.06", True)
        + para("GPA：2.98/4.0（专业前 50%）", size=19, after=42)
        + bullet("全国大学生数学建模大赛赛区二等奖；蓝桥杯全国软件和信息技术专业人才大赛赛区三等奖；大学生校园创新创业校级奖项。")
    )


def campus():
    return (
        section("补充经历")
        + two_col("内蒙古大学学生社区团工委 | 宣传教育部干事", "2020.09 - 2021.10", True)
        + bullet("参与中秋佳节、趣味运动会、校园藏宝等活动策划与执行，负责海报、推文、汇报 PPT 和现场协同。")
        + two_col("图书馆档案室 | 档案室助理", "2022.10 - 2023.07", True)
        + bullet("整理学生档案、按年限上架并录入系统，保证档案类别、基础信息和检索状态准确。")
    )


def doc_xml(parts):
    sect = (
        "<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/>"
        "<w:pgMar w:top=\"560\" w:right=\"720\" w:bottom=\"560\" w:left=\"720\" "
        "w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr>"
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        "<w:body>" + "".join(parts) + sect + "</w:body></w:document>"
    )


def write_docx(path, parts):
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        "</Relationships>"
    )
    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    )
    if PHOTO.exists():
        doc_rels += (
            '<Relationship Id="rIdPhoto" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            'Target="media/resume_photo.jpg"/>'
        )
    doc_rels += "</Relationships>"
    types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="jpg" ContentType="image/jpeg"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )
    path = Path(path)
    if path.exists():
        path.unlink()
    with ZipFile(path, "w", ZIP_DEFLATED) as zip_file:
        zip_file.writestr("[Content_Types].xml", types)
        zip_file.writestr("_rels/.rels", rels)
        zip_file.writestr("word/_rels/document.xml.rels", doc_rels)
        zip_file.writestr("word/document.xml", doc_xml(parts))
        if PHOTO.exists():
            zip_file.write(PHOTO, "word/media/resume_photo.jpg")
    print(path.resolve(), os.path.getsize(path))


def cpp_resume():
    summary = (
        section("个人简介")
        + para("后端工程师，主要参与金融行情链路中的指数、股票等行情业务处理、行情处理框架调优及行情数据存储框架调整。具备 C++ 后端服务开发、数据处理链路设计、性能排查与稳定性优化经验，关注低延迟、高吞吐、可维护的数据服务建设。", size=20, after=50)
    )
    skills = section("专业技能")
    for item in [
        "后端开发：C/C++、Python、SQL，熟悉面向对象设计、数据结构、多线程/异步处理、服务拆分与模块化设计。",
        "行情业务：理解指数、股票等行情数据的接入、清洗、转换、分发、存储和回放链路，能围绕业务规则处理数据质量与一致性问题。",
        "性能优化：具备日志分析、链路追踪、瓶颈定位、内存与线程模型优化经验，能针对吞吐、延迟和稳定性做专项调优。",
        "工具平台：Git、Linux、Oracle、Hadoop、OpenStack、HTML；英语 CET-6。",
    ]:
        skills += bullet(item)
    work = experience(
        "万得信息技术股份有限公司",
        "2024.07 - 至今",
        "后端工程师",
        "上海",
        [
            "参与金融行情后端服务研发，围绕指数、股票等行情品种建设业务处理、框架优化和数据存储能力。",
            "负责核心链路中的需求分析、方案设计、编码实现、联调验证和问题排查，保障行情处理链路稳定运行。",
            "持续优化服务可维护性和处理效率，沉淀通用组件、处理规范和排障经验，降低后续业务接入成本。",
        ],
        [
            ("指数和股票等行情业务处理服务", "任职期间", "核心开发", "C++、SQL、Linux、行情数据处理", [
                "面向指数、股票等行情业务建设后端处理服务，完成数据接入、字段标准化、业务规则计算、状态维护与结果输出。",
                "梳理不同行情品种的数据结构和处理差异，将通用逻辑抽象为可复用模块，提升新增业务接入效率。",
                "针对行情数据异常、缺失、重复和时序不一致等场景补充校验与容错处理，提升下游使用稳定性。",
                "配合联调和线上问题排查，结合日志、样本数据和业务规则定位问题，保障行情链路准确性和连续性。",
            ]),
            ("行情处理框架调优", "任职期间", "核心开发", "C++、多线程、异步处理、性能分析", [
                "对行情处理框架的关键路径进行梳理，识别数据解析、分发、队列堆积、日志输出等可能影响吞吐与延迟的环节。",
                "优化模块调用关系和数据流转方式，减少重复解析、无效拷贝和不必要的同步等待，提升处理链路整体效率。",
                "补充关键指标和诊断日志，形成可观测的排查路径，便于快速定位峰值行情、异常数据和下游阻塞问题。",
                "在保证业务兼容的前提下推进渐进式调优，降低框架调整对既有行情服务的影响。",
            ]),
            ("行情数据存储框架调整", "任职期间", "核心开发", "C++、SQL、存储框架、数据一致性", [
                "参与行情数据存储框架调整，围绕写入路径、表结构/分区、批量落库和历史数据回放需求优化整体设计。",
                "梳理不同品种和频率行情数据的存储差异，统一关键字段、索引和生命周期管理策略，提升数据可查询性。",
                "优化数据写入与异常重试流程，减少重复写入、漏写和格式不一致问题，增强存储链路可靠性。",
                "配合上下游验证数据准确性，支持行情业务处理结果的追溯、回放和问题复盘。",
            ]),
        ],
    )
    older = section("早期项目")
    older += project_block("进程调度算法模拟系统", "2022.11 - 2022.12", "全权负责", "C++、EasyX、操作系统调度算法", [
        "实现先来先服务、短进程优先、优先级、时间片轮转等调度策略，并通过界面展示调度过程与结果。",
    ])
    older += project_block("图书馆管理系统 / 选课系统 / 停车场管理系统", "2021.02 - 2021.10", "全权负责", "C++、数据结构、权限模型", [
        "完成用户角色、权限控制、借还/选退课/车辆进出等业务流程，强化面向对象设计、函数封装、栈和队列应用。",
    ])
    return [header("后端工程师 | C++ 行情系统方向"), summary, skills, work, older, education(), campus()]


def agent_resume():
    summary = (
        section("个人简介")
        + para("后端工程师，聚焦 Java/Python 后端与 AI Agent 平台建设，参与 AliceToHome Agent 服务平台、Wind 智能市场（AIMarket）及行情类 Agent 能力建设。熟悉 Agent 服务编排、工具/MCP/Skill 接入、金融行情能力封装和平台化交付，能将业务接口沉淀为可复用的智能体能力。", size=20, after=50)
    )
    skills = section("专业技能")
    for item in [
        "后端开发：Java、Python、C/C++、SQL，具备服务接口设计、模块化开发、平台能力封装和工程化交付经验。",
        "Agent 平台：熟悉 Agent 服务编排、工具调用、MCP 接入、Skill 能力组织、行情类智能体封装与多 Agent 场景落地。",
        "金融数据：理解行情数据查询、指标/品种能力抽象、用户意图到工具调用的映射，以及结果结构化返回与展示。",
        "工具平台：Git、Linux、HTML、Oracle、Hadoop、OpenStack、TensorFlow、OpenCV；英语 CET-6。",
    ]:
        skills += bullet(item)
    work = experience(
        "万得信息技术股份有限公司",
        "2024.07 - 至今",
        "后端工程师",
        "上海",
        [
            "参与 AI Agent 与金融行情能力平台建设，负责后端服务、工具能力封装、MCP/Skill 接入和行情类 Agent 落地。",
            "将万得金融数据与内部服务能力抽象为可调用工具，支持智能体根据用户意图完成查询、分析和结果组织。",
            "参与平台联调、问题排查与能力迭代，提升 Agent 服务的可扩展性、稳定性和复用效率。",
        ],
        [
            ("Agent 服务平台 AliceToHome", "任职期间", "核心开发", "Java、Python、Agent、工具编排、服务平台", [
                "参与搭建 AliceToHome Agent 服务平台，支持 Agent 创建、工具接入、服务编排、调用链路管理和能力扩展。",
                "设计并实现工具/能力注册与调用流程，将后端接口、业务服务和数据能力包装为智能体可调用的标准能力。",
                "围绕 Agent 执行链路补充参数校验、异常处理、日志追踪和结果结构化输出，提升平台排障效率和可维护性。",
                "支持不同业务场景的 Agent 快速接入，降低单独开发智能体服务的重复成本。",
            ]),
            ("Wind 智能市场 AIMarket", "任职期间", "核心开发", "Java、Python、MCP、Skill、Agent、金融行情", [
                "参与搭建 Wind 智能市场（AIMarket），围绕金融数据查询、行情分析和智能体能力市场化组织平台功能。",
                "接入并维护万得 MCP 与 Skill 能力，将行情、指标、品种和分析接口封装为可被 Agent 调用的工具集合。",
                "设计行情类 Agent 的能力边界和调用流程，支持独立行情查询、组合查询、结果解释和后续分析扩展。",
                "配合平台侧完成能力上架、调试、示例构建和问题定位，让业务能力以更低成本复用到不同 Agent 场景。",
            ]),
            ("独立行情类 Agent 能力建设", "任职期间", "核心开发", "Python、Java、行情接口、Agent 工具链", [
                "面向股票、指数等行情场景构建单独行情类 Agent，将用户自然语言问题映射到行情查询、字段选择和结果组织流程。",
                "封装行情数据查询工具，统一入参、出参和错误提示，提升不同 Agent 之间的能力复用和调用一致性。",
                "优化返回内容结构，使 Agent 输出同时满足用户可读性和下游系统继续处理的结构化要求。",
            ]),
        ],
    )
    older = section("早期项目")
    older += project_block("基于爬虫的开源软件缺陷预测", "2024.01 - 2024.03", "全权负责", "Python、LDA、聚类、HTML、Git", [
        "爬取应用商店用户评论并完成清洗、分类和主题提取，通过网页展示缺陷主题、分类和预测结果。",
    ])
    older += project_block("AI 看图说话", "2023.07 - 2023.08", "组长 | 东软集团实训", "Python、TensorFlow、CNN、EfficientNetB1", [
        "负责框架搭建、模型测试、数据增强和参数调整，完成图片特征提取与描述生成流程。",
    ])
    return [header("后端工程师 | Agent / Java / Python 方向"), summary, skills, work, older, education(), campus()]


if __name__ == "__main__":
    write_docx("于艳波_后端工程师_C++行情方向_简历.docx", cpp_resume())
    write_docx("于艳波_后端工程师_Agent方向_简历.docx", agent_resume())
