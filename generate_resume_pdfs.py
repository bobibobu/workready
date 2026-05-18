from pathlib import Path
import html


ROOT = Path(__file__).resolve().parent
PHOTO = ROOT / "resume_photo.jpg"


def h(text):
    return html.escape(text, quote=True)


def bullet(text):
    return f"<li>{h(text)}</li>"


def section(title):
    return f"<h2>{h(title)}</h2>"


def project(title, date, meta, bullets):
    return (
        f"<div class='project'>"
        f"<div class='row'><h3>{h(title)}</h3><span>{h(date)}</span></div>"
        f"<p class='meta'>{h(meta)}</p>"
        f"<ul>{''.join(bullet(x) for x in bullets)}</ul>"
        f"</div>"
    )


def base_html(title, summary, skills, projects, role_line):
    photo_html = ""
    if PHOTO.exists():
        photo_html = f"<img class='photo' src='{PHOTO.as_uri()}' alt='photo'>"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{h(title)}</title>
<style>
@page {{ size: A4; margin: 8mm 15mm; }}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  color: #1f1f1f;
  font-family: "Microsoft YaHei", "SimSun", "PingFang SC", Arial, sans-serif;
  font-size: 9.42pt;
  line-height: 1.39;
}}
.page {{ position: relative; max-width: 180mm; margin: 0 auto; }}
.header {{ min-height: 78px; padding-right: 86px; }}
h1 {{ margin: 0 0 2px; font-size: 21.4pt; line-height: 1.05; font-weight: 800; }}
.target {{ color: #1f4e79; font-size: 12pt; font-weight: 700; margin-bottom: 4px; }}
.contact, .edu-line {{ color: #444; font-size: 8.95pt; margin: 1.7px 0; }}
.photo {{ position: absolute; top: 0; right: 0; width: 68px; height: 88px; object-fit: cover; }}
h2 {{
  margin: 7px 0 4px;
  padding-bottom: 2.7px;
  border-bottom: 1.25px solid #5b9bd5;
  font-size: 13.25pt;
  line-height: 1.15;
  font-weight: 800;
}}
h3 {{ margin: 0; font-size: 10.3pt; line-height: 1.21; font-weight: 800; }}
p {{ margin: 0 0 3.2px; }}
ul {{ margin: 2.2px 0 4px 16px; padding: 0; }}
li {{ margin: 0 0 1.6px; padding-left: 1px; }}
.row {{ display: flex; justify-content: space-between; align-items: baseline; gap: 14px; }}
.row span {{ white-space: nowrap; color: #444; font-size: 9pt; }}
.meta {{ color: #444; font-size: 9pt; margin: 0.7px 0 2.7px; }}
.project {{ break-inside: avoid; margin-bottom: 4.2px; }}
.summary {{ margin-bottom: 3.2px; }}
.work-head {{ margin-bottom: 3.2px; }}
.work-head .meta {{ margin-top: 1px; }}
.compact-head {{ margin-top: 1px; }}
</style>
</head>
<body>
<main class="page">
  <header class="header">
    {photo_html}
    <h1>于艳波</h1>
    <div class="target">{h(title)}</div>
    <p class="contact">电话：182-4806-1241&nbsp;&nbsp;&nbsp;&nbsp;邮箱：3272871858@qq.com&nbsp;&nbsp;&nbsp;&nbsp;城市：上海</p>
    <p class="edu-line">本科 | 软件工程 | 内蒙古大学（211） | 英语 CET-6</p>
  </header>

  {section("个人简介")}
  <p class="summary">{h(summary)}</p>

  {section("教育背景")}
  <div class="row"><h3>内蒙古大学（211） | 软件工程 | 本科</h3><span>2020.09 - 2024.06</span></div>
  <ul>{bullet("英语 CET-6；全国大学生数学建模大赛赛区二等奖；蓝桥杯全国软件和信息技术专业人才大赛赛区三等奖。")}</ul>

  {section("专业技能")}
  <ul>{''.join(bullet(x) for x in skills)}</ul>

  {section("工作经历")}
  <div class="work-head">
    <div class="row"><h3>万得信息技术股份有限公司</h3><span>2024.08 - 至今</span></div>
    <p class="meta">{h(role_line)} | 上海</p>
  </div>
  {projects}
</main>
</body>
</html>"""


def agent_html():
    summary = (
        "后端工程师，聚焦 Java/Python 后端与 AI Agent 平台工程化落地。参与 AliceToHome Agent 服务平台、"
        "Wind 智能市场（AIMarket）及行情类 Agent 能力建设，核心负责短期记忆、上下文 Context、后台管理、"
        "Skill/MCP 能力开发等模块，并参与网关调用链路建设，具备将金融数据、RAG 检索与通用对话能力封装为可复用 Agent 工具的实践经验。"
    )
    skills = [
        "后端开发：Java、Python、SQL，具备 RESTful 接口设计、服务拆分、网关链路、接口联调、异常处理、日志排查和工程化交付经验。",
        "Agent 工程：熟悉 Agent 创建/配置、短期记忆、上下文 Context、Function Calling、MCP Server、Skill、JSON Schema、工具注册、调用链日志和结构化输出。",
        "数据与检索：参与行情数据 MCP、RAG 数据 MCP 开发，理解证券识别、市场确认、字段选择、行情查询、资料检索和结果组织流程。",
        "工具平台：Git、Linux、Oracle，具备后端服务部署、联调和线上问题排查经验。",
    ]
    intro = project("工作概览", "", "后端开发工程师", [
        "参与 AI Agent 与金融行情能力平台建设，承担后端服务开发、工具能力封装、MCP/Skill 接入、联调验证和线上问题排查。",
        "完成 2 个 MCP（行情数据、RAG 数据）、14 个 Skill 和 1 个通用对话 Agent 的开发/接入，沉淀工具注册、参数校验、错误提示和结果结构化输出流程。",
    ])
    projects = intro + project("Agent 服务平台 AliceToHome", "2025.12 - 2026.03", "核心开发 | Java、Python、Agent、工具编排、Context", [
        "核心负责后端短期记忆与上下文 Context 模块，围绕会话标识、历史消息、工具调用结果和用户意图维护多轮对话状态。",
        "设计上下文组装与透传流程，将系统指令、用户问题、历史轮次、工具结果和能力返回按执行链路组织，并结合上下文裁剪控制输入长度。",
        "统一工具描述、入参 schema、出参结构、错误提示和结构化结果输出，减少工具接入时的重复适配，为后续 Skill/MCP 能力复用提供标准口径。",
    ]) + project("Wind 智能市场 AIMarket", "2026.03 - 至今", "后台管理负责人 / 核心开发 | Java、Python、MCP、Skill、金融行情", [
        "负责 AIMarket 后台管理模块建设，围绕 2 个 MCP、14 个 Skill 和 1 个通用对话 Agent 提供配置维护、上下线管理、版本维护和平台化组织能力。",
        "协助开发网关调用链路，参与请求校验、traceId 透传、路由分发、能力调用、超时控制、异常映射和结构化结果返回等后端流程。",
        "完成行情数据 MCP、RAG 数据 MCP 及 14 个 Skill 的开发/维护，统一能力描述、参数校验、错误码和返回结构，覆盖行情查询、资料检索、通用问答和能力编排等 4 类场景。",
    ]) + project("通用对话 Agent 与 Skill/MCP 能力建设", "2026.03 - 至今", "核心开发 | Python、Java、MCP、Skill、Function Calling", [
        "开发 1 个通用对话 Agent，接入行情数据 MCP、RAG 数据 MCP 和多类 Skill 能力，支持普通问答、资料检索与行情数据查询。",
        "面向股票、指数等行情场景构建工具调用链路，将自然语言问题拆解为证券识别、市场确认、字段选择、行情查询、RAG 检索和结果组织。",
        "围绕 Skill/MCP 沉淀能力描述、入参/出参 schema、默认参数补全、异常返回和结果裁剪策略，提升工具复用、调用一致性和下游系统解析效率。",
    ])
    return base_html("后端工程师 | Agent 平台 / Java / Python 方向", summary, skills, projects, "后端开发工程师")


def cpp_html():
    summary = (
        "C++ 后端开发工程师，聚焦金融行情链路开发，核心参与指数模块研发，并协助跨市场行情衍生模块建设。"
        "具备 A 股、港股、美股等全市场行情数据处理经验，熟悉分钟线、日线和行情衍生指标计算，能够围绕实时性、"
        "数据一致性、性能瓶颈定位和稳定性治理推进工程落地。"
    )
    skills = [
        "C++ 后端：C/C++（C++11/14）、STL、多线程/异步编程、内存管理、模块拆分、接口联调，具备 Linux 环境下服务开发与问题排查经验。",
        "行情系统：理解 A 股、港股、美股行情数据接入、标准化、业务规则计算、分发、存储、回放链路，能处理缺失、重复、乱序等数据质量问题。",
        "性能排障：熟悉 gdb、perf、pmap/top、FlameGraph，具备 CPU、内存、IO、队列堆积、日志链路排查经验；了解 Valgrind/Massif、ASan/LSan 等内存分析工具。",
        "数据存储：熟悉 SQL、Oracle，参与行情数据写入路径、表结构/分区、批量落库、索引和生命周期管理优化。",
    ]
    intro = project("工作概览", "", "C++ 后端开发工程师", [
        "参与金融行情后端服务研发，核心负责指数模块开发，并协助跨市场行情衍生模块建设。",
        "覆盖 A 股、港股、美股等全市场行情链路，日均处理约 5000 个代码，单代码每日约 242 条分钟线，仅分钟线基础数据约 121 万条/日，并支撑 OHLC、成交量、成交额及衍生指标等千万级字段处理。",
    ])
    projects = intro + project("指数行情业务处理服务", "2024.08 - 2024.12", "指数模块核心开发 | C++、SQL、Linux、行情数据处理", [
        "面向指数、股票等行情业务建设后端处理服务，完成数据接入、字段标准化、业务规则计算、状态维护与结果输出。",
        "支持 A 股、港股、美股等市场数据处理，覆盖分钟线、日线、行情衍生指标等数据形态，按市场、品种、交易日和交易阶段组织处理规则，支撑约 121 万条/日分钟线基础数据处理。",
        "围绕代码、交易日、时间戳、OHLC、成交量、成交额和衍生指标构建校验逻辑，处理缺失、重复、乱序、字段格式不一致等异常数据，保障下游计算与落库一致性。",
    ]) + project("跨市场行情衍生模块与框架调优", "2025.01 - 2025.06", "协助开发 / 核心开发 | C++、多线程、异步队列、性能分析", [
        "围绕 W 量比等行情衍生指标优化计算框架，将原先主要面向 A 股股票的队列计算流程扩展为支持 A 股股票、指数和海外股票指数同步计算。",
        "基于多线程与生产者-消费者队列模型拆解指标计算链路，按市场/品种维度隔离任务分发，并通过任务分片降低单一队列阻塞对整体链路的影响。",
        "在约 121 万条分钟线回放压测中，对比优化前后处理耗时、队列长度和下游写入状态，单轮处理耗时由约 18 分钟降至约 10 分钟，峰值队列堆积下降约 50%。",
        "补充处理耗时、队列长度、异常数据量、下游写入状态等关键日志，形成从接入、计算、分发到写入的排查路径，便于按市场、品种和队列定位峰值行情下的链路瓶颈。",
    ]) + project("行情数据存储框架调整与线上问题排查", "2025.06 - 2025.12", "核心开发 | C++、SQL、存储框架、火焰图、内存分析", [
        "参与行情数据存储框架调整，围绕写入路径、表结构/分区、批量落库和历史回放需求优化整体设计。",
        "梳理不同品种和频率行情数据的存储差异，统一关键字段、索引和生命周期管理策略，减少重复写入、漏写和格式不一致风险。",
        "处理线上内存暴增问题，通过复现模拟、pmap/top 观察进程内存、gdb/perf 采样和火焰图定位异常分配路径，区分真实泄漏、缓存增长和对象生命周期问题；修复后在连续 6 小时回放压测中内存曲线趋于稳定，未再出现线性增长。",
    ])
    return base_html("后端工程师 | C++ 行情系统方向", summary, skills, projects, "C++ 后端开发工程师")


def write_html():
    outputs = [
        ("于艳波_后端工程师_Agent方向_简历.html", agent_html()),
        ("于艳波_后端工程师_C++行情方向_简历.html", cpp_html()),
    ]
    for name, content in outputs:
        path = ROOT / name
        path.write_text(content, encoding="utf-8")
        print(path)


if __name__ == "__main__":
    write_html()
