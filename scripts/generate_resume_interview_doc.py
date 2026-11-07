from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape
import os


OUT = Path("简历补充信息与模拟面试问答.docx")
BLUE = "1F4E79"
DARK = "222222"
GRAY = "666666"


def esc(text):
    return escape(str(text), {'"': "&quot;"})


def r(text, bold=False, size=21, color=DARK):
    b = "<w:b/>" if bold else ""
    return (
        f"<w:r><w:rPr>{b}<w:color w:val=\"{color}\"/>"
        f"<w:sz w:val=\"{size}\"/><w:szCs w:val=\"{size}\"/>"
        f"<w:rFonts w:ascii=\"Calibri\" w:hAnsi=\"Calibri\" "
        f"w:eastAsia=\"Microsoft YaHei\" w:cs=\"Microsoft YaHei\"/>"
        f"</w:rPr><w:t xml:space=\"preserve\">{esc(text)}</w:t></w:r>"
    )


def p(text="", bold=False, size=21, after=80, before=0, color=DARK, left=0, hanging=0):
    ind = f"<w:ind w:left=\"{left}\" w:hanging=\"{hanging}\"/>" if left or hanging else ""
    return (
        f"<w:p><w:pPr><w:spacing w:before=\"{before}\" w:after=\"{after}\" "
        f"w:line=\"300\" w:lineRule=\"auto\"/>{ind}</w:pPr>"
        f"{r(text, bold, size, color)}</w:p>"
    )


def title(text):
    return p(text, True, 34, after=120, color="000000")


def section(text):
    return (
        f"<w:p><w:pPr><w:spacing w:before=\"160\" w:after=\"70\"/>"
        f"<w:pBdr><w:bottom w:val=\"single\" w:sz=\"8\" w:space=\"4\" "
        f"w:color=\"{BLUE}\"/></w:pBdr></w:pPr>{r(text, True, 28, '000000')}</w:p>"
    )


def sub(text):
    return p(text, True, 23, after=60, before=80, color=BLUE)


def bullet(text):
    return p("• " + text, size=20, after=46, left=420, hanging=210)


def qa(question, answer):
    return p("Q：" + question, True, 20, after=36) + p("A：" + answer, size=20, after=90, left=260)


def content():
    parts = []
    parts.append(title("简历补充信息与模拟面试问答"))
    parts.append(p("适用对象：于艳波 | 后端工程师 | C++ 行情系统方向 / Agent Java Python 方向", size=20, color=GRAY))
    parts.append(p("说明：以下内容分为“我可以基于现有经历帮你补强的内容”和“必须由你确认的数据”。涉及具体指标、线上规模、公司内部系统细节的部分，建议确认后再写进正式简历。", size=20))

    parts.append(section("一、我能帮你补充的信息"))
    parts.append(sub("1. 可以直接补强的简历表达"))
    for item in [
        "把“参与项目”改成更有工程含量的表达：需求分析、方案设计、核心模块实现、联调验证、线上问题排查、稳定性优化。",
        "把万得经历前置，学生项目压缩到“早期项目/补充项目”，让简历从应届项目型转为工作经历型。",
        "为 C++ 版强化关键词：行情链路、指数/股票行情、数据接入、业务规则处理、低延迟、高吞吐、框架调优、存储一致性。",
        "为 Agent 版强化关键词：Agent 服务平台、AliceToHome、AIMarket、MCP、Skill、工具编排、行情类 Agent、Java/Python 后端。",
        "补充个人简介，让面试官第一眼知道你现在不是泛泛的软件工程师，而是有金融行情和智能体平台经历的后端工程师。",
    ]:
        parts.append(bullet(item))

    parts.append(sub("2. 可以合理推断但建议你确认后使用的内容"))
    for item in [
        "万得任职时间：我暂按“2024.07 - 至今”处理，如果实际入职时间不同，需要替换。",
        "工作地点：我暂写“上海”，如果实际为南京、杭州、远程或其他地点，需要替换。",
        "项目角色：当前写法为“核心开发”，如果你是 owner、模块负责人、主要开发或参与开发，需要精确调整。",
        "技术栈：C++ 版可补 Linux、多线程、异步队列、SQL、存储框架；Agent 版可补 Java、Python、MCP、Skill、工具调用、平台服务。具体框架如 Spring Boot、FastAPI、Redis、Kafka 等必须按真实情况填写。",
        "成果描述：可以写“提升效率、增强稳定性、降低接入成本”，但最好补具体指标，否则不要写成百分比。",
    ]:
        parts.append(bullet(item))

    parts.append(sub("3. 最需要你补充的硬信息"))
    for item in [
        "C++ 行情项目：支持哪些市场或品种？A 股、港股、美股、指数、ETF、基金、债券？",
        "行情处理规模：日均/峰值处理多少条行情？峰值 QPS 或 TPS？平均延迟或最大延迟是多少？",
        "框架调优结果：CPU、内存、延迟、吞吐、队列堆积、失败率有没有优化前后对比？",
        "存储框架调整：使用什么数据库或存储？Oracle、MySQL、Redis、Kafka、文件存储、自研存储？解决了写入慢、重复写、查询慢还是回放困难？",
        "AliceToHome：你负责哪些模块？Agent 管理、工具注册、权限、日志、调用链、配置中心、评测、模型网关？",
        "AIMarket：万得 MCP 和 Skill 具体包含多少工具/能力？覆盖哪些行情查询和分析场景？你做了哪些接口封装或标准化？",
        "Agent 效果：是否有工具调用成功率、响应时延、接入 Agent 数量、Skill 数量、用户/内部团队使用情况？",
    ]:
        parts.append(bullet(item))

    parts.append(section("二、模拟面试官问题与参考答案"))
    parts.append(sub("A. 通用开场"))
    parts.append(qa(
        "请你做一下自我介绍。",
        "面试官您好，我叫于艳波，本科毕业于内蒙古大学软件工程专业，目前在万得信息技术股份有限公司担任后端工程师。我的工作主要有两条线：一条是金融行情后端，包括指数、股票等行情业务处理服务、行情处理框架调优和行情数据存储框架调整；另一条是 AI Agent 平台，包括 AliceToHome Agent 服务平台、Wind 智能市场 AIMarket，以及万得 MCP、Skill 和行情类 Agent 能力建设。我比较熟悉 C++ 后端服务、Java/Python 平台开发，以及把金融数据能力封装成可复用工具的工程化流程。"
    ))
    parts.append(qa(
        "你为什么想看新的机会？",
        "我希望继续在后端工程和 AI Agent 结合的方向上深入。一方面，我有金融行情链路的工程经验，理解实时数据处理、稳定性和性能优化的重要性；另一方面，我也参与过 Agent 平台和工具能力建设，希望在更复杂的业务场景里继续做平台化、工程化和智能化能力落地。"
    ))

    parts.append(sub("B. C++ 行情系统方向"))
    cpp_qas = [
        ("你做的指数和股票行情业务处理服务主要解决什么问题？",
         "这个服务主要负责把上游接入的指数、股票等行情数据进行标准化处理，并根据业务规则完成字段转换、状态维护、异常校验和结果输出。我的工作重点是理解不同品种的字段差异和处理规则，把通用逻辑抽象出来，同时对缺失、重复、乱序等数据问题做容错处理，保证下游拿到的数据稳定、准确、可追溯。"),
        ("行情业务处理中最容易出问题的地方是什么？",
         "我认为主要有三类：第一是数据质量问题，比如缺失、重复、乱序、字段格式不一致；第二是业务规则问题，比如不同品种、不同市场、不同交易阶段的处理逻辑不完全一致；第三是链路稳定性问题，比如高峰数据量下队列堆积、处理延迟增加、下游写入或消费变慢。处理这类问题时，我一般会先确认数据样本和业务规则，再结合日志和链路指标定位问题发生在哪一层。"),
        ("你做行情处理框架调优时，通常怎么定位性能瓶颈？",
         "我会先把链路拆成接入、解析、转换、分发、写入几个阶段，观察每个阶段的耗时、队列长度、异常日志和资源占用。然后重点看是否存在重复解析、频繁内存拷贝、锁竞争、同步等待、日志过量或下游阻塞。如果是框架级调优，我会优先做低风险改动，比如减少无效处理、补充关键指标、优化数据流转方式，再逐步验证吞吐和延迟变化。"),
        ("C++ 服务里你如何考虑稳定性？",
         "我会从几个层面考虑：输入侧要做参数和数据合法性校验，处理侧要避免异常数据影响整条链路，输出侧要有失败处理和必要的重试/降级机制；同时关键路径要有日志和指标，方便出问题时快速定位。对于高频行情场景，还要关注内存增长、队列堆积、线程阻塞和下游服务慢调用。"),
        ("行情数据存储框架调整的价值是什么？",
         "行情数据不仅要实时处理，也要支持查询、回放和问题复盘。存储框架调整的价值在于统一不同品种和频率数据的写入规范、字段结构和异常处理方式，减少重复写、漏写、格式不一致等问题，同时提升后续查询和追溯效率。"),
        ("如果让你设计一个行情处理服务，你会怎么设计？",
         "我会拆成接入层、解析标准化层、业务规则处理层、分发层和存储层。接入层负责协议和数据源适配；标准化层统一字段和格式；业务层处理品种规则、交易状态和衍生字段；分发层面向不同下游输出；存储层负责实时写入、历史回放和一致性校验。关键路径上要有日志、指标、限流和异常隔离。"),
    ]
    for q, a in cpp_qas:
        parts.append(qa(q, a))

    parts.append(sub("C. Agent / Java / Python 方向"))
    agent_qas = [
        ("AliceToHome Agent 服务平台主要做什么？",
         "AliceToHome 的核心是把 Agent 的创建、工具接入、能力编排、调用链路和结果输出平台化。我的理解是，它不是单个 Agent，而是一个支撑多个 Agent 场景复用的服务平台。我的工作会围绕后端能力封装、工具注册调用、参数校验、异常处理、日志追踪和结果结构化输出展开。"),
        ("AIMarket 和普通聊天机器人有什么区别？",
         "AIMarket 更像金融能力市场和智能体平台，重点不是泛泛聊天，而是把万得金融数据、行情查询、分析能力、MCP 和 Skill 组织成可被 Agent 调用的工具集合。用户的问题会被转成具体的数据能力调用，再把结构化结果组织成可读答案。因此它更强调工具准确性、金融数据边界、结果可信度和能力复用。"),
        ("你怎么理解 MCP 和 Skill？",
         "MCP 更偏向标准化的工具/资源访问协议，让模型或 Agent 能以统一方式调用外部能力；Skill 更像面向具体任务封装的一组操作说明、工具流程和领域能力。放在 AIMarket 里，MCP 可以承载万得金融数据接口，Skill 可以把某类金融分析或行情查询流程组织成可复用能力。"),
        ("Agent 调用工具时最常见的问题是什么？",
         "常见问题包括意图识别不准、工具选择错误、参数缺失或格式不对、接口返回异常、结果太长或结构不适合展示。工程上需要通过工具描述、参数 schema、默认值/补全逻辑、错误提示、日志追踪和结果结构化来降低这些问题。"),
        ("如何评估一个行情类 Agent 做得好不好？",
         "我会看几个指标：工具选择是否准确、参数抽取是否正确、返回数据是否可信、回答是否能解释字段含义、异常时是否能给出明确提示，以及响应时延是否可接受。如果有条件，还可以建立典型问题集，统计调用成功率、答案正确率和平均响应时间。"),
        ("如果用户问“帮我看一下某只股票最近表现”，Agent 应该怎么处理？",
         "首先识别证券代码或名称，并确认市场；然后判断用户想看的是行情走势、涨跌幅、成交量、估值还是新闻事件。如果问题不明确，可以先给出默认分析维度，比如最新价、区间涨跌幅、成交额、相对指数表现和关键风险提示。底层通过行情工具获取结构化数据，再组织成简洁结论。"),
        ("你做 Agent 平台时如何保证可扩展性？",
         "我会把 Agent、工具、参数、权限、日志和结果格式拆开设计。新增能力时，尽量只需要注册工具、定义参数 schema、补充描述和示例，而不是改 Agent 主流程。对于金融场景，还要把品种、市场、指标等能力边界定义清楚，避免不同 Agent 重复实现同一套查询逻辑。"),
    ]
    for q, a in agent_qas:
        parts.append(qa(q, a))

    parts.append(sub("D. 简历追问与风险问题"))
    risk_qas = [
        ("你简历里写“框架调优”，具体优化了什么？",
         "建议回答真实优化点。如果暂时没有量化数据，可以说：我主要参与的是链路梳理、关键路径排查、减少重复处理、补充诊断日志和优化数据流转方式。后续如果有准确指标，可以补充优化前后的吞吐、延迟、CPU 或内存变化。"),
        ("你在项目里是主导还是参与？",
         "不要夸大。可以回答：整体方案由团队共同确定，我主要负责其中的某些模块开发、联调和问题排查。如果某个模块确实由你独立完成，再明确说“这个模块由我负责设计和实现”。"),
        ("你对金融业务理解到什么程度？",
         "可以回答：我目前主要理解行情处理链路和部分品种数据规则，包括指数、股票等行情数据的接入、字段标准化、异常处理、存储和下游使用。更复杂的交易、风控或估值业务还在持续学习。这样诚实但不显弱。"),
        ("你最大的短板是什么？",
         "可以回答：我现在还在补足更系统的架构设计和复杂线上问题治理经验。过去更多是在具体模块和链路优化中积累，现在会主动从稳定性、可观测性、扩展性和数据一致性角度复盘项目。"),
        ("为什么你同时投 C++ 和 Agent？会不会方向不聚焦？",
         "可以回答：我的底层能力是后端工程，C++ 行情系统让我理解高性能数据链路，Agent 项目让我理解如何把业务能力平台化、工具化。两个方向不是割裂的，金融 Agent 最终仍然依赖稳定的数据服务和后端工程能力。根据岗位不同，我会突出不同项目。"),
    ]
    for q, a in risk_qas:
        parts.append(qa(q, a))

    parts.append(section("三、正式投递前建议补齐的 12 个数字"))
    for item in [
        "入职时间、工作地点、当前职级/岗位名称。",
        "C++ 行情服务覆盖的品种数量、市场数量、字段/接口数量。",
        "行情链路日均数据量、峰值数据量、峰值 QPS/TPS。",
        "调优前后延迟、吞吐、CPU、内存、队列堆积、失败率任意 2-3 个指标。",
        "存储框架使用的数据库/中间件名称，以及写入速度或查询效率变化。",
        "AliceToHome 支持的 Agent 数量、工具数量、接入业务数量。",
        "AIMarket 中万得 MCP 的工具数量、Skill 数量、覆盖场景。",
        "行情类 Agent 的典型问题集规模、调用成功率或响应时间。",
        "你独立负责的模块名称和代码/接口边界。",
        "线上故障或疑难问题排查案例 1-2 个。",
        "团队规模，以及你和产品、测试、前端、算法的协作方式。",
        "是否有获奖、专利、内部表彰、绩效、用户反馈等证明材料。",
    ]:
        parts.append(bullet(item))
    return parts


def write_docx():
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        "</Relationships>"
    )
    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>'
    )
    types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body>"
        + "".join(content())
        + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="720" w:right="780" w:bottom="720" w:left="780" '
        'w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>'
        + "</w:body></w:document>"
    )
    if OUT.exists():
        OUT.unlink()
    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/document.xml", document)
    print(OUT.resolve())
    print(os.path.getsize(OUT))


if __name__ == "__main__":
    write_docx()
