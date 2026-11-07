from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
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


def para(text="", bold=False, size=20, after=62, before=0, color=DARK, align=None, left=0, hanging=0):
    align_tag = f"<w:jc w:val=\"{align}\"/>" if align else ""
    ind = f"<w:ind w:left=\"{left}\" w:hanging=\"{hanging}\"/>" if left or hanging else ""
    return (
        f"<w:p><w:pPr><w:spacing w:before=\"{before}\" w:after=\"{after}\" "
        f"w:line=\"276\" w:lineRule=\"auto\"/>{align_tag}{ind}</w:pPr>"
        f"{run(text, bold, size, color)}</w:p>"
    )


def bullet(text):
    return para("• " + text, size=19, after=36, left=360, hanging=180)


def section(title):
    return (
        f"<w:p><w:pPr><w:spacing w:before=\"96\" w:after=\"46\"/>"
        f"<w:pBdr><w:bottom w:val=\"single\" w:sz=\"8\" w:space=\"4\" "
        f"w:color=\"{BLUE}\"/></w:pBdr></w:pPr>{run(title, True, 25, '000000')}</w:p>"
    )


def table_row(cells, widths, bold=None, sizes=None, after=22):
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


def two_col(left, right="", bold_left=False, bold_right=False, left_width=6500, right_width=2200):
    return (
        "<w:tbl><w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders><w:top w:val=\"nil\"/><w:left w:val=\"nil\"/>"
        "<w:bottom w:val=\"nil\"/><w:right w:val=\"nil\"/>"
        "<w:insideH w:val=\"nil\"/><w:insideV w:val=\"nil\"/></w:tblBorders>"
        "</w:tblPr>"
        + table_row([left, right], [left_width, right_width], [bold_left, bold_right], [21, 20], 16)
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
        para("于艳波", True, 36, 16)
        + para(target, True, 22, 36, color=BLUE)
        + para("电话：182-4806-1241    邮箱：3272871858@qq.com    城市：上海", size=19, after=30, color=GRAY)
        + para("本科 | 软件工程 | 内蒙古大学 | 英语 CET-6", size=19, after=10, color=GRAY)
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


def project_block(name, date, role, stack, bullets):
    out = two_col(name, date, True, False)
    out += para(f"{role} | 技术栈：{stack}", size=19, after=32, color=GRAY)
    for item in bullets:
        out += bullet(item)
    return out


def education():
    return (
        section("教育背景")
        + two_col("内蒙古大学（211） | 软件工程 | 本科", "2020.09 - 2024.06", True)
        + bullet("英语 CET-6；全国大学生数学建模大赛赛区二等奖；蓝桥杯全国软件和信息技术专业人才大赛赛区三等奖。")
    )


def older_agent_projects():
    return (
        section("早期项目")
        + project_block("基于爬虫的开源软件缺陷预测", "2024.01 - 2024.03", "全权负责", "Python、LDA、聚类、HTML、Git", [
            "完成用户评论爬取、清洗、分类与主题提取，并通过网页展示缺陷主题、分类和预测结果。",
        ])
        + project_block("AI 看图说话", "2023.07 - 2023.08", "组长 | 东软集团实训", "Python、TensorFlow、CNN、EfficientNetB1", [
            "负责框架搭建、模型测试、数据增强和参数调整，完成图片特征提取与描述生成流程。",
        ])
    )


def older_cpp_projects():
    return (
        section("早期项目")
        + project_block("进程调度算法模拟系统", "2022.11 - 2022.12", "全权负责", "C++、EasyX、操作系统调度算法", [
            "实现先来先服务、短进程优先、优先级、时间片轮转等调度策略，并通过界面展示调度过程与结果。",
        ])
        + project_block("图书馆管理系统 / 选课系统", "2021.02 - 2021.09", "全权负责", "C++、数据结构、权限模型", [
            "完成用户角色、权限控制、借还/选退课等业务流程，强化面向对象设计、函数封装和数据结构应用。",
        ])
    )


def agent_resume():
    summary = (
        section("个人简介")
        + para("后端工程师，聚焦 Java/Python 后端与 AI Agent 平台工程化落地。参与 AliceToHome Agent 服务平台、Wind 智能市场（AIMarket）及行情类 Agent 能力建设，核心负责短期记忆、上下文 Context、后台管理、Skill/MCP 能力开发等模块，并参与网关调用链路建设，具备将金融数据、RAG 检索与通用对话能力封装为可复用 Agent 工具的实践经验。", size=20, after=48)
    )
    skills = section("专业技能")
    for item in [
        "后端开发：Java、Python、SQL，具备 RESTful 接口设计、服务拆分、网关链路、接口联调、异常处理、日志排查和工程化交付经验。",
        "Agent 工程：熟悉 Agent 创建/配置、短期记忆、上下文 Context、Function Calling、MCP Server、Skill、JSON Schema、工具注册、调用链日志和结构化输出。",
        "数据与检索：参与行情数据 MCP、RAG 数据 MCP 开发，理解证券识别、市场确认、字段选择、行情查询、资料检索和结果组织流程。",
        "工具平台：Git、Linux、Oracle，具备后端服务部署、联调和线上问题排查经验。",
    ]:
        skills += bullet(item)
    work = (
        section("工作经历")
        + two_col("万得信息技术股份有限公司", "2024.08 - 至今", True)
        + para("后端开发工程师 | 上海", size=20, after=36, color=GRAY)
        + bullet("参与 AI Agent 与金融行情能力平台建设，承担后端服务开发、工具能力封装、MCP/Skill 接入、联调验证和线上问题排查。")
        + bullet("完成 2 个 MCP（行情数据、RAG 数据）、14 个 Skill 和 1 个通用对话 Agent 的开发/接入，沉淀工具注册、参数校验、错误提示和结果结构化输出流程。")
        + project_block("Agent 服务平台 AliceToHome", "2025.12 - 2026.03", "核心开发", "Java、Python、Agent、工具编排、Context", [
            "参与 Agent 服务平台建设，核心负责后端短期记忆与上下文 Context 模块，围绕会话标识、历史消息、工具调用结果和用户意图维护多轮对话状态。",
            "设计上下文组装与透传流程，将系统指令、用户问题、历史轮次、工具结果和能力返回按执行链路组织，并结合上下文裁剪控制输入长度。",
            "统一工具描述、入参 schema、出参结构、错误提示和结构化结果输出，减少工具接入时的重复适配，为后续 Skill/MCP 能力复用提供标准口径。",
        ])
        + project_block("Wind 智能市场 AIMarket", "2026.03 - 至今", "后台管理负责人 / 核心开发", "Java、Python、MCP、Skill、金融行情", [
            "负责 AIMarket 后台管理模块建设，围绕 2 个 MCP、14 个 Skill 和 1 个通用对话 Agent 提供配置维护、上下线管理、版本维护和平台化组织能力。",
            "协助开发网关调用链路，参与请求校验、traceId 透传、路由分发、能力调用、超时控制、异常映射和结构化结果返回等后端流程。",
            "完成行情数据 MCP、RAG 数据 MCP 及 14 个 Skill 的开发/维护，统一能力描述、参数校验、错误码和返回结构，覆盖行情查询、资料检索、通用问答和能力编排等 4 类场景。",
        ])
        + project_block("通用对话 Agent 与 Skill/MCP 能力建设", "2026.03 - 至今", "核心开发", "Python、Java、MCP、Skill、Function Calling", [
            "开发 1 个通用对话 Agent，接入行情数据 MCP、RAG 数据 MCP 和多类 Skill 能力，支持普通问答、资料检索与行情数据查询。",
            "面向股票、指数等行情场景构建工具调用链路，将自然语言问题拆解为证券识别、市场确认、字段选择、行情查询、RAG 检索和结果组织。",
            "围绕 Skill/MCP 沉淀能力描述、入参/出参 schema、默认参数补全、异常返回和结果裁剪策略，提升工具复用、调用一致性和下游系统解析效率。",
        ])
    )
    return [header("后端工程师 | Agent 平台 / Java / Python 方向"), summary, education(), skills, work]


def cpp_resume():
    summary = (
        section("个人简介")
        + para("C++ 后端开发工程师，聚焦金融行情链路开发，核心参与指数模块研发，并协助跨市场行情衍生模块建设。具备 A 股、港股、美股等全市场行情数据处理经验，熟悉分钟线、日线和行情衍生指标计算，能够围绕实时性、数据一致性、性能瓶颈定位和稳定性治理推进工程落地。", size=20, after=48)
    )
    skills = section("专业技能")
    for item in [
        "C++ 后端：C/C++（C++11/14）、STL、多线程/异步编程、内存管理、模块拆分、接口联调，具备 Linux 环境下服务开发与问题排查经验。",
        "行情系统：理解 A 股、港股、美股行情数据接入、标准化、业务规则计算、分发、存储、回放链路，能处理缺失、重复、乱序等数据质量问题。",
        "性能排障：熟悉 gdb、perf、pmap/top、FlameGraph，具备 CPU、内存、IO、队列堆积、日志链路排查经验；了解 Valgrind/Massif、ASan/LSan 等内存分析工具。",
        "数据存储：熟悉 SQL、Oracle，参与行情数据写入路径、表结构/分区、批量落库、索引和生命周期管理优化。",
    ]:
        skills += bullet(item)
    work = (
        section("工作经历")
        + two_col("万得信息技术股份有限公司", "2024.08 - 至今", True)
        + para("C++ 后端开发工程师 | 上海", size=20, after=36, color=GRAY)
        + bullet("参与金融行情后端服务研发，核心负责指数模块开发，并协助跨市场行情衍生模块建设。")
        + bullet("覆盖 A 股、港股、美股等全市场行情链路，日均处理约 5000 个代码，单代码每日约 242 条分钟线，仅分钟线基础数据约 121 万条/日，并支撑 OHLC、成交量、成交额及衍生指标等千万级字段处理。")
        + project_block("指数行情业务处理服务", "2024.08 - 2024.12", "指数模块核心开发", "C++、SQL、Linux、行情数据处理", [
            "面向指数、股票等行情业务建设后端处理服务，完成数据接入、字段标准化、业务规则计算、状态维护与结果输出。",
            "支持 A 股、港股、美股等市场数据处理，覆盖分钟线、日线、行情衍生指标等数据形态，按市场、品种、交易日和交易阶段组织处理规则，支撑约 121 万条/日分钟线基础数据处理。",
            "围绕代码、交易日、时间戳、OHLC、成交量、成交额和衍生指标构建校验逻辑，处理缺失、重复、乱序、字段格式不一致等异常数据，保障下游计算与落库一致性。",
        ])
        + project_block("跨市场行情衍生模块与框架调优", "2025.01 - 2025.06", "协助开发 / 核心开发", "C++、多线程、异步队列、性能分析", [
            "围绕 W 量比等行情衍生指标优化计算框架，将原先主要面向 A 股股票的队列计算流程扩展为支持 A 股股票、指数和海外股票指数同步计算。",
            "基于多线程与生产者-消费者队列模型拆解指标计算链路，按市场/品种维度隔离任务分发，并通过任务分片降低单一队列阻塞对整体链路的影响。",
            "在约 121 万条分钟线回放压测中，对比优化前后处理耗时、队列长度和下游写入状态，单轮处理耗时由约 18 分钟降至约 10 分钟，峰值队列堆积下降约 50%。",
            "补充处理耗时、队列长度、异常数据量、下游写入状态等关键日志，形成从接入、计算、分发到写入的排查路径，便于按市场、品种和队列定位峰值行情下的链路瓶颈。",
        ])
        + project_block("行情数据存储框架调整与线上问题排查", "2025.06 - 2025.12", "核心开发", "C++、SQL、存储框架、火焰图、内存分析", [
            "参与行情数据存储框架调整，围绕写入路径、表结构/分区、批量落库和历史回放需求优化整体设计。",
            "梳理不同品种和频率行情数据的存储差异，统一关键字段、索引和生命周期管理策略，减少重复写入、漏写和格式不一致风险。",
            "处理线上内存暴增问题，通过复现模拟、pmap/top 观察进程内存、gdb/perf 采样和火焰图定位异常分配路径，区分真实泄漏、缓存增长和对象生命周期问题；修复后在连续 6 小时回放压测中内存曲线趋于稳定，未再出现线性增长。",
        ])
    )
    return [header("后端工程师 | C++ 行情系统方向"), summary, education(), skills, work]


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


if __name__ == "__main__":
    write_docx("于艳波_后端工程师_Agent方向_简历.docx", agent_resume())
    write_docx("于艳波_后端工程师_C++行情方向_简历.docx", cpp_resume())
