# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 下午8:24
# @Author  : xianfa
# @FileName: 这次绝对不跑路.py
# @Software: PyCharm
from models import Test, db, College, Class, Subject, Student, Major, Teacher, Page
import random, time

db.drop_all()
db.create_all()

students_data = \
    {
        "计算机科学与工程学院":
            {
                "计算机科学与技术": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "物联网工程": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "智能科学与技术": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "智能科学与技术(中外交流)": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "软件工程(3E实验班)": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "计算机实验班": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
            },
        "化工与制药学院":
            {
                "化学工程与工艺": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "化学工程与工艺(中外交流)": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "化学工程与工艺(卓越交流)": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "制药工程": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "制药工程(卓越工程师)": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "能源化学工程": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "生物工程": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "药物制剂": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "生物技术": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "食品科学与工程": {"2015": {}, "2016": {}, "2017": {}, "2018": {}}
            },
        "法商学院":
            {
                "法学": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "国际经济与贸易": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "经济学": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "法商双专业实验班": {"2015": {}, "2016": {}, "2017": {}, "2018": {}}
            },
        "管理学院":
            {
                "行政管理": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "公共事业管理": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "工商管理": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "工商管理体育经济与管理方向": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "市场营销": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "会计学(ACCA方案)": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "会计学(中外交流)": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "信息管理与信息系统": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "财务管理": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "电子商务": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "'英语+会计'专业": {"2015": {}, "2016": {}, "2017": {}, "2018": {}}
            },
        "外语学院":
            {
                "英语": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "汉语国际教育": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "'英语+法学'双专业": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "'英语+市场营销'双专业": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "'英语+化学工程与工艺'双专业": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "'英语+软件工程'双专业": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
                "'英语+日语'双专业": {"2015": {}, "2016": {}, "2017": {}, "2018": {}},
            }
    }

last_names = (
    '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨'
    '朱秦尤许何吕施张孔曹严华金魏陶姜'
    '戚谢邹喻柏水窦章云苏潘葛奚范彭郎'
    '鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
    '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常'
    '乐于时傅皮卞齐康伍余元卜顾孟平黄'
)

first_names = {
    'male': [
        '致远', '俊驰', '雨泽', '烨磊', '晟睿',
        '天佑', '文昊', '修洁', '黎昕', '远航',
        '旭尧', '鸿涛', '伟祺', '荣轩', '越泽',
        '浩宇', '瑾瑜', '皓轩', '浦泽', '绍辉',
        '绍祺', '升荣', '圣杰', '晟睿', '思聪'
    ],
    'female': [
        '沛玲', '欣妍', '佳琦', '雅芙', '雨婷',
        '韵寒', '莉姿', '雨婷', '宁馨', '妙菱',
        '心琪', '雯媛', '诗婧', '露洁', '静琪',
        '雅琳', '灵韵', '清菡', '溶月', '素菲',
        '雨嘉', '雅静', '梦洁', '梦璐', '惠茜'
    ]
}

subjects = ["计算机程序设计基础", "离散结构", "面向对象程序设计", "算法与数据结构", "计算机组成原理", "计算机网络", "操作系统", "数字逻辑", "数据库原理与应用", "算法设计与分析",
            "嵌入式系统（计算机）", "人工智能", "机器人控制原理", "模拟电子技术（计算机）", "数字图像处理（计算机）", "机器视觉（32学时_2）", "虚拟现实技术", "智能计算（计算机）",
            "工业检测技术", "工业机器人技术"]

tests = {"数据库原理与应用": {
    "choice_question": [
        {"question": "现实世界中事物在某一方面的特性在信息世界中称为__________。", "A": "实体", "B": "实体值", "C": "属性", "D": "信息", "answer": "C",
         "level": 1},
        {"question": "数据的存储结构与数据逻辑结构之间的独立性称为数据的__________。", "A": "结构独立性", "B": "物理独立性", "C": "逻辑独立性", "D": "分布独立性",
         "answer": "B", "level": 1},
        {"question": "要保证数据库的逻辑数据独立性，需要修改的是___。", "A": "模式与外模式之间的映射", "B": "模式与内模式之间的映射", "C": "模式", "D": "三级模式",
         "answer": "A", "level": 1},
        {"question": "数据库系统的数据独立性体现在__。", "A": "不会因为数据的变化而影响到应用程序", "B": "不会因为数据存储结构与数据逻辑结构的变化而影响应用程序",
         "C": "不会因为存储策略的变化而影响存储结构", "D": "不会因为某些存储结构的变化而影响其他的存储结构", "answer": "B", "level": 1},
        {"question": "关系数据模型是目前最重要的一种数据模型，它的三个要素分别是__。", "A": "实体完整性、参照完整性、用户自定义完整性", "B": "数据结构、关系操作、完整性约束",
         "C": "数据增加、数据修改、数据查询", "D": "外模式、模式、内模式", "answer": "B", "level": 1},
        {"question": "__的存取路径对用户透明，从而具有更高的数据独立性、更好的安全保密性，也简化了程序员的工作和数据库开发建立的工作。", "A": "网状模型", "B": "关系模型", "C": "层次模型",
         "D": "以上都有", "answer": "B", "level": 2},
        {"question": "要保证数据库的数据独立性，需要修改的是__", "A": "模式与外模式", "B": "模式与内模式", "C": "三级模式之间的两层映射", "D": " 三层模式",
         "answer": "C", "level": 2},
        {"question": "概念模型是现实世界的第一层抽象，这一类模型中最著名的模型是__", "A": "层次模型", "B": "关系模型", "C": " 网状模型", "D": "实体-关系模型",
         "answer": "D", "level": 2},
        {"question": "下述__不是DBA数据库管理员的职责 。", "A": "完整性约束说明", "B": "定义数据库模式", "C": "数据库安全", "D": "数据库管理系统设计",
         "answer": "D",
         "level": 2},
        {"question": "下面列出的数据库管理技术发展的三个阶段中，没有专门的软件对数据进行管理的是___。 I．人工管理阶段 II．文件系统阶段 III．数据库阶段", "A": " I 和 II",
         "B": "只有 II",
         "C": " II 和 II", "D": "只有 I", "answer": "D", "level": 2},
        {"question": "数据库的概念模型独立于____", "A": "具体的机器和DBMS", "B": "E-R图", "C": "信息世界", "D": "现实世界", "answer": "A",
         "level": 3},
        {"question": "在数据库技术中，面向对象数据模型是一种____", "A": "概念模型", "B": "结构模型", "C": "物理模型", "D": "形象模型", "answer": "A",
         "level": 3},
        {"question": "数据模型用来表示实体间的联系，但不同的数据库管理系统支持不同的数据模型。在常用的数据模型中，不包括____", "A": "网状模型", "B": "链状模型", "C": "层次模型",
         "D": "关系模型", "answer": "B", "level": 3},
        {"question": "在数据管理技术的发展过程中，经历了人工管理阶段、文件系统阶段和数据库系统阶段。在这几个阶段中，数据独立的最高的是____阶段", "A": "数据库系统", "B": "文件系统",
         "C": "人工管理", "D": " 数据项管理", "answer": "A", "level": 3},
    ],
    "true_false_question": [
        {"question": "SQL Server 2000，Access，Oracle等DBMS，都是面向对象的数据库管理系统。（ ）", "answer": "0", "level": 1},
        {"question": "在关系数据模型中，只有一种结构——关系。不论是实体还是实体之间的联系都是用关系来表达的。( )", "answer": "0", "level": 1},
        {"question": "一个数据库只能对应一个应用程序，即一个数据库只能为一个应用程序所用。（    ）", "answer": "0", "level": 1},
        {"question": "SQL语言是SQL Server数据库管理系统的专用语言，其它的数据库如Oracle、Sybase等都不支持这种语言。（   ）", "answer": "0", "level": 2},
        {"question": "对于一个基本关系表来说，列的顺序无所谓——即改变属性的排列顺序不会改变该关系的本质结构。（   ）", "answer": "1", "level": 2},
        {"question": "对于一个基本关系表来说，行的顺序无所谓——即将一条记录插入在第一行和插入在第五行没有本质上的不同。（   ）", "answer": "1", "level": 2},
        {"question": "在一个关系表上最多只能建立一个聚簇索引。（  ）", "answer": "1", "level": 1},
        {"question": "若.一个数据库管理系统提供了强制存取控制机制（MAC），则它一定也会提供自主存取控制机制。（  ）", "answer": "1", "level": 1},
        {"question": "在开发一个数据库应用系统的时候，无论什么时候，都是设计的数据库范式越高越好。（  ）", "answer": "0", "level": 2},
        {"question": "一个全码的关系模式，其范式一定达到了三范式。（     )", "answer": "1", "level": 2},
        {"question": "微软公司发布的Microsoft SQL Server 2008是一个非关系型数据库管理系统。(  )", "answer": "0", "level": 3},
        {"question": "在关系数据模型中，二维表的列称为属性，二维表的行称为元组。（   ）", "answer": "1", "level": 3},
        {"question": "在SQL Server 2008中，一个数据库至少需要有一个数据文件和一个事务日志文件。（  ）", "answer": "1", "level": 3},
        {"question": "分离数据库时，数据库被从磁盘上删除了。（ ）", "answer": "0", "level": 3},
        {"question": "数据库是长期储存在计算机内、有组织的、可共享的大量数据的集合。(  ）", "answer": "1", "level": 3}

    ],
    "fill_blank_question": [
        {"question": "SQL Server 2008系统由4部分组成，这4个部分被称为4个服务，分别是_____、分析服务、报表服务和集成服务。", "answer": ["数据库引擎"], "level": 2},
        {"question": "SQL Server 2008系统提供了两种类型的数据库，即__系统数据库_和______。", "answer": ["用户数据库"], "level": 2},
        {"question": "在SQL Server 2008中，主数据未年检的后缀是__.mdf_，事务日志文件的后缀是_.ldf_。辅助文件的后缀___", "answer": [".ndf"], "level": 2},
        {"question": "使用_create_database__语句创建数据库，创建数据库之后，也可以根据需要使用_______ 语句对数据库进行修改。", "answer": ["alter database"],
         "level": 2},
        {"question": ".目前，数据库领域常用的数据模型有层次模型、网状模型和____模型。", "answer": ["关系"], "level": 2},
        {"question": "在T-SQL中，用alter table语句修改表的结构，用______句修改表中的数据。", "answer": ["insert select"], "level": 3},
        {"question": "用户自定义函数包括表值函数和__标量值_函数两类，其中表值函数又包括内联表值函数和_____函数。", "answer": ["多语句表值"], "level": 1},
        {"question": "聚合函数AVG返回一组值的平均值，_____返回一组值中项目的数量。", "answer": ["count"], "level": 2},
        {"question": "EXISTS称为存在量词，在WHERE子句中使用EXISTS，表示当子查询的结果_____存在时，条件为TRUE。", "answer": ["非空"], "level": 2},
        {"question": "从历史发展看来，数据管理技术经历了人工管理、   文件管理   和  ________  三个阶段。", "answer": ["数据库管理"], "level": 1},
        {"question": "在SQL语言中，用符号  —  代表单个字符，用符号 _______ 代表0到多个字符。", "answer": ["%"], "level": 3},
        {"question": ".在SQL语言中，为了使查询的结果表中不包含完全相同的两个元组，应在select的后面加上关键词 ________ 。", "answer": ["distinct"], "level": 1},
        {"question": "在数据库设计中，若关系模式设计得范式太低，可能会使得数据库存在数据冗余、修改复杂 、 插入异常和删除异常 四个方面的弊端。采取的解决方法就是对该关系模式进行 _________ 。",
         "answer": ["分解"], "level": 2},
        {"question": "根据关系理论，对一个关系模式的最起码的要求是满足_______。", "answer": ["范式"], "level": 3},
        {"question": "如果一个关系模式中不存在  非主属性对码（或候选码) 的 ________，则该关系模式就达到了二范式。", "answer": ["部分函数依赖"], "level": 1},
        {"question": " 关系的完整性一般包括实体完整性规则 和_______和  自定义完整性规则 ", "answer": ["参照完整性"], "level": 2},
        {"question": '数据库与文件系统的根本区别是_______________。', "answer": ["数据的结构化"], "level": 1},
        {"question": " SQL Server提供了动态的自我管理机制，能够自动增大或缩小数据库所占用的 _____ 。", "answer": ["硬盘空间"], "level": 3},
        {"question": "数据模型有层次模型、网状模型、关系模型。当前主流数据库系统采用_______。", "answer": ["关系模型"], 'level': 3},
        {"question": "实体完整性是指关系中的____ 不允许取空值。", "answer": ["主键"], "level": 3}
    ],
    "free_response_question": [
        {"question": "", "answer": "", "level": 2}
    ]}
}
college_code = 9
for college_name in students_data.keys():
    college = College()
    college.name = college_name
    db.session.add(college)
    college_code += 1
    major_code = 9
    print(college_name)
    for major_name in students_data[college_name].keys():
        major = Major()
        major.name = major_name
        college.majors.append(major)
        major_code += 1
        print(major_name)
        for grade in students_data[college_name][major_name].keys():
            print(grade)
            for class_code in range(10, 15):
                class_name = grade + "级" + major_name + str(class_code) + "班"
                class_ = Class()
                class_.name = class_name
                major.classes.append(class_)
                print(class_name)
                for student_code in range(10, 30):
                    last_name = random.choice(last_names)
                    sex = random.choice(["male", "female"])
                    first_name = random.choice(first_names[sex])
                    name = last_name + first_name
                    student = Student()
                    student.name = name
                    student.id = int(
                        grade[-2:] + str(college_code) + str(major_code) + str(class_code) + str(student_code))
                    student.grade = int(grade)
                    student.password_hash = "pbkdf2:sha256:150000$LssWNeqi$de05643547efe747ad0a14b74ac2e0e036e2d21fcae3be98bd43c94392f2226d"
                    class_.students.append(student)

for subject_name in tests.keys():
    subject = Subject()
    subject.name = subject_name
    db.session.add(subject)
    print(subject_name)
    for type_name in tests[subject_name].keys():
        for test_item in tests[subject_name][type_name]:
            test = Test()
            test.type_ = type_name
            if type_name == "choice_question":
                test.question = test_item["question"] + "\nA." + test_item["A"] + "\nB." + \
                                test_item["B"] + "\nC." + test_item[
                                    "C"] + "\nD." + test_item["D"]
            else:
                test.question = test_item["question"]
            if tests[subject_name] == "fill_blank_question":
                answer = ""
                for blank in test_item["answer"]:
                    answer += blank
            else:
                answer = test_item["answer"]
            test.answer = answer
            test.level = test_item["level"]
            subject.tests.append(test)

for i in range(84001, 84111):
    teacher = Teacher()
    teacher.id = i
    last_name = random.choice(last_names)
    sex = random.choice(["male", "female"])
    first_name = random.choice(first_names[sex])
    name = last_name + first_name
    teacher.name = name
    teacher.password_hash = "pbkdf2:sha256:150000$LssWNeqi$de05643547efe747ad0a14b74ac2e0e036e2d21fcae3be98bd43c94392f2226d"
    db.session.add(teacher)
db.session.commit()
