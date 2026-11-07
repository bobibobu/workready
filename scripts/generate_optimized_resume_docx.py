from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape
import os


OUT = Path("于艳波_简历_优化版.docx")
PHOTO = Path("resume_photo.jpg")

BLUE = "2F75B5"
TEXT = "222222"


def x(text):
    return escape(str(text), {'"': "&quot;"})


def r(text, bold=False, size=21, color=TEXT):
    b = "<w:b/>" if bold else ""
    return (
        f"<w:r><w:rPr>{b}<w:color w:val=\"{color}\"/>"
        f"<w:sz w:val=\"{size}\"/><w:szCs w:val=\"{size}\"/>"
        f"<w:rFonts w:ascii=\"Calibri\" w:hAnsi=\"Calibri\" "
        f"w:eastAsia=\"Microsoft YaHei\" w:cs=\"Microsoft YaHei\"/>"
        f"</w:rPr><w:t xml:space=\"preserve\">{x(text)}</w:t></w:r>"
    )


def p(text="", bold=False, size=21, spacing_after=80, indent_left=0, hanging=0, color=TEXT):
    ind = ""
    if indent_left or hanging:
        ind = f"<w:ind w:left=\"{indent_left}\" w:hanging=\"{hanging}\"/>"
    return (
        f"<w:p><w:pPr><w:spacing w:after=\"{spacing_after}\" w:line=\"300\" "
        f"w:lineRule=\"auto\"/>{ind}</w:pPr>{r(text, bold, size, color)}</w:p>"
    )


def bullet(text):
    return p("• " + text, size=20, spacing_after=45, indent_left=420, hanging=210)


def section(title):
    return (
        f"<w:p><w:pPr><w:spacing w:before=\"120\" w:after=\"70\"/>"
        f"<w:pBdr><w:bottom w:val=\"single\" w:sz=\"8\" w:space=\"4\" "
        f"w:color=\"{BLUE}\"/></w:pBdr></w:pPr>{r(title, True, 30, '000000')}</w:p>"
    )


def two_col(left, right="", bold_left=False, bold_right=False):
    widths = [5200, 2600]
    return (
        "<w:tbl><w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders><w:top w:val=\"nil\"/><w:left w:val=\"nil\"/>"
        "<w:bottom w:val=\"nil\"/><w:right w:val=\"nil\"/>"
        "<w:insideH w:val=\"nil\"/><w:insideV w:val=\"nil\"/></w:tblBorders>"
        "</w:tblPr><w:tr>"
        f"<w:tc><w:tcPr><w:tcW w:w=\"{widths[0]}\" w:type=\"dxa\"/></w:tcPr>"
        f"{p(left, bold_left, 22, 30)}</w:tc>"
        f"<w:tc><w:tcPr><w:tcW w:w=\"{widths[1]}\" w:type=\"dxa\"/></w:tcPr>"
        f"{p(right, bold_right, 22, 30)}</w:tc>"
        "</w:tr></w:tbl>"
    )


def project(title, date, role, location, bullets):
    body = [two_col(title, date, True, False), p(f"{role} | {location}", size=20, spacing_after=55)]
    body.extend(bullet(item) for item in bullets)
    body.append(p("", spacing_after=70))
    return "".join(body)


def info_table():
    photo = ""
    if PHOTO.exists():
        photo = (
            "<w:p><w:r><w:drawing><wp:inline xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
            "distT=\"0\" distB=\"0\" distL=\"0\" distR=\"0\">"
            "<wp:extent cx=\"860000\" cy=\"1146000\"/><wp:docPr id=\"1\" name=\"photo\"/>"
            "<a:graphic xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\">"
            "<a:graphicData uri=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">"
            "<pic:pic xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">"
            "<pic:nvPicPr><pic:cNvPr id=\"0\" name=\"resume_photo.jpg\"/><pic:cNvPicPr/></pic:nvPicPr>"
            "<pic:blipFill><a:blip r:embed=\"rIdPhoto\" xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\"/>"
            "<a:stretch><a:fillRect/></a:stretch></pic:blipFill>"
            "<pic:spPr><a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"860000\" cy=\"1146000\"/></a:xfrm>"
            "<a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom></pic:spPr>"
            "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>"
        )
    rows = [
        ("姓名：于艳波", "性别：男"),
        ("学历：本科", "年龄：24"),
        ("电话：182-4806-1241", "邮箱：3272871858@qq.com"),
        ("城市：呼和浩特", "求职意向：软件开发 / 数据分析 / 大数据开发"),
    ]
    cells = ""
    for left, right in rows:
        cells += (
            "<w:tr>"
            "<w:tc><w:tcPr><w:tcW w:w=\"3500\" w:type=\"dxa\"/></w:tcPr>"
            f"{p(left, size=22, spacing_after=70)}</w:tc>"
            "<w:tc><w:tcPr><w:tcW w:w=\"4200\" w:type=\"dxa\"/></w:tcPr>"
            f"{p(right, size=22, spacing_after=70)}</w:tc>"
            "</w:tr>"
        )
    return (
        "<w:tbl><w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders><w:top w:val=\"nil\"/><w:left w:val=\"nil\"/>"
        "<w:bottom w:val=\"nil\"/><w:right w:val=\"nil\"/>"
        "<w:insideH w:val=\"nil\"/><w:insideV w:val=\"nil\"/></w:tblBorders>"
        "</w:tblPr><w:tr><w:tc><w:tcPr><w:tcW w:w=\"7900\" w:type=\"dxa\"/></w:tcPr>"
        f"<w:tbl><w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/></w:tblPr>{cells}</w:tbl>"
        "</w:tc><w:tc><w:tcPr><w:tcW w:w=\"1300\" w:type=\"dxa\"/></w:tcPr>"
        f"{photo}</w:tc></w:tr></w:tbl>"
    )


def document_xml():
    content = []
    content.append(section("基本信息"))
    content.append(info_table())
    content.append(section("教育背景"))
    content.append(two_col("内蒙古大学 | 软件工程 | 本科", "2020.09 - 2024.06", True))
    content.append(p("GPA：2.98/4.0（专业前 50%）", size=20, spacing_after=45))
    content.append(bullet("全国大学生数学建模大赛赛区二等奖；蓝桥杯全国软件和信息技术专业人才大赛赛区三等奖；大学生校园创新创业校级奖项。"))

    content.append(section("专业技能"))
    for item in [
        "编程与开发：熟悉 C/C++、Python、SQL，具备面向对象设计、数据结构与算法、操作系统调度模拟等项目实践。",
        "数据与算法：了解机器学习、LDA 主题模型、聚类、KNN、α-β剪枝、CNN 图像处理等方法，能完成数据清洗、特征处理与结果展示。",
        "工具与平台：使用过 Git、HTML、TensorFlow、OpenCV、Oracle、Hadoop、OpenStack、EasyX、Photoshop 等工具或平台。",
        "语言与证书：英语 CET-6；持有机动车驾驶证。",
    ]:
        content.append(bullet(item))

    content.append(section("项目经历"))
    projects = [
        ("基于爬虫的开源软件缺陷预测", "2024.01 - 2024.03", "全权负责", "呼和浩特", [
            "使用 Python 爬取应用商店用户评论，按软件类别进行数据整理、清洗和标注，为缺陷预测提供数据基础。",
            "基于用户评论进行 LDA 主题提取和聚类分析，总结高频缺陷主题与用户痛点，形成可解释的预测结果。",
            "搭建完整演示系统，通过 HTML 页面展示分类、主题分析和预测结果；项目中规范使用 Git 管理代码版本。",
        ]),
        ("AI 看图说话", "2023.07 - 2023.08", "组长 | 东软集团实训", "天津", [
            "负责项目框架搭建、模型测试、数据增强和参数调整，协调组员推进图像描述生成任务。",
            "对带标注图片进行特征提取与向量化处理，引入词典和文本序列建模，支撑图片内容描述生成。",
            "在 TensorFlow 框架下使用 EfficientNetB1 等 CNN 模型训练图片特征，结合锐化、变色、翻转、镜像等增强方式提升拟合效果。",
        ]),
        ("进程调度算法模拟系统", "2022.11 - 2022.12", "全权负责", "呼和浩特", [
            "使用 C++ 模拟先来先服务、短进程优先、优先级、时间片轮转等操作系统调度算法。",
            "支持输入进程名、占用时长、优先级和权重，并可选择抢占式与非抢占式调度策略。",
            "使用 EasyX 设计简洁交互界面，将进程执行过程和调度结果可视化展示。",
        ]),
        ("五子棋人机对战", "2022.07 - 2022.09", "组长", "呼和浩特", [
            "使用 Python 实现五子棋人机对战逻辑，完成棋盘、背景和交互界面的图形化展示。",
            "通过棋型评分选择最优落子，并尝试 KNN、α-β剪枝与神经网络思路优化决策效果。",
            "在项目推进中负责方案拆解和组员沟通，提升了 Python 应用、机器学习基础和团队协作能力。",
        ]),
        ("图书馆管理系统", "2021.07 - 2021.09", "全权负责", "呼和浩特", [
            "使用 C++ 实现图书借阅、归还、库存更新等日常管理功能。",
            "设计学生、教师、管理员等角色及权限控制，保证不同角色仅能访问对应操作。",
            "通过函数封装和递归调用拆分业务流程，提高代码复用性和功能扩展性。",
        ]),
        ("内蒙古大学选课系统（模拟）", "2021.02 - 2021.03", "全权负责", "呼和浩特", [
            "使用 C++ 模拟学生选课系统，完成学生、教师、管理员三类角色建模。",
            "实现登录校验、密码管理、课程查询、选课退课、课程及学生信息增删改查等功能。",
            "通过循环、函数调用和权限分层组织业务逻辑，强化了面向对象和基础数据结构实践。",
        ]),
        ("停车场管理系统", "2021.09 - 2021.10", "全权负责", "呼和浩特", [
            "使用 C++ 实现车辆入场、出场及停车状态管理。",
            "结合栈和队列模拟停车场与候车区管理流程，加深了对数据结构和指针机制的理解。",
        ]),
    ]
    for item in projects:
        content.append(project(*item))

    content.append(section("校园与实践经历"))
    content.append(project("内蒙古大学学生社区团工委", "2020.09 - 2021.10", "干事 | 宣传教育部", "呼和浩特", [
        "参与策划并执行中秋佳节、趣味运动会、校园藏宝等校园活动，累计吸引上千名学生参与。",
        "负责宣传海报、推文和汇报 PPT 制作，配合团队完成活动宣传、现场组织和复盘工作。",
        "在校园藏宝活动中带领约 50 名学生参与，锻炼了沟通协调、现场组织和任务推进能力。",
    ]))
    content.append(project("图书馆档案室", "2022.10 - 2023.07", "档案室助理", "呼和浩特", [
        "根据档案室规范整理学生档案，完成类别规整、按年限上架和信息校对。",
        "将学生档案信息录入档案室系统，提升档案检索和后续管理效率。",
    ]))

    sect = (
        "<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/>"
        "<w:pgMar w:top=\"680\" w:right=\"820\" w:bottom=\"680\" w:left=\"820\" "
        "w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr>"
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        "<w:body>" + "".join(content) + sect + "</w:body></w:document>"
    )


def write_docx():
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
            '<Relationship Id="rIdPhoto" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            'Target="media/resume_photo.jpg"/>'
        )
    doc_rels += "</Relationships>"
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="jpg" ContentType="image/jpeg"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )

    if OUT.exists():
        OUT.unlink()
    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/document.xml", document_xml())
        if PHOTO.exists():
            z.write(PHOTO, "word/media/resume_photo.jpg")
    print(OUT.resolve())
    print(os.path.getsize(OUT))


if __name__ == "__main__":
    write_docx()
