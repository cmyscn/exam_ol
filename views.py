from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from forms import LoginForm, RegisterFormStudent, RegisterFormTeacher, StudentInfoForm, TeacherInfoForm, TestCreaterForm
from models import app, Student, Teacher, College, Major, Subject, Plan, Page, Test, Class, TestType, Admin, db


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template("登录页面.html", form=form)


@app.route("/studentMenu", methods=['GET', 'POST'])
def studentMenu():
    return render_template("学生菜单.html")


@app.route("/teacherMenu", methods=['GET', 'POST'])
def teacherMenu():
    return render_template("教师菜单.html")


@app.route("/adminMenu", methods=['GET', 'POST'])
def adminMenu():
    return render_template("管理员菜单.html")


@app.route("/teacherManager", methods=['GET', 'POST'])
def teacherManager():
    return render_template("教师管理页面.html")


@app.route('/studentManager', methods=['GET', 'POST'])
def studentManager():
    return render_template("学生管理页面.html")


@app.route('/testManager', methods=['GET', 'POST'])
def testManager():
    return render_template("考试管理页面.html")


@app.route("/testPage/<int:page_id>/", methods=['GET', 'POST'])
def testPage(page_id):
    return render_template("考试答题页面.html")


@app.route("/testQuery", methods=['GET', 'POST'])
def testQuery():
    tests = [{"第一次考试": 1}, {"第二次考试": 2}]
    return render_template("考试查询页面.html", tests=tests)


@app.route("/teacherSignUp", methods=['GET', 'POST'])
def teacherSignUp():
    form = RegisterFormTeacher()
    return render_template("教师注册页面.html", form=form)


@app.route("/studentSignUp", methods=['GET', 'POST'])
def studentSignUp():
    form = RegisterFormStudent()
    form.college.choices = [(1, '测试')]
    form.major.choices = [(1, '测试')]
    form.grade.choices = [(1, '测试')]
    form.classes.choices = [(1, '测试')]
    return render_template("学生注册页面.html", form=form)


@app.route("/teacherInfo", methods=['GET', 'POST'])
def teacherInfo():
    form = TeacherInfoForm()
    return render_template("教师信息页面.html", form=form)


@app.route("/studentInfo", methods=['GET', 'POST'])
def studentInfo():
    form = StudentInfoForm()
    form.college.choices = [(1, '测试')]
    form.major.choices = [(1, '测试')]
    form.grade.choices = [(1, '测试')]
    form.classes.choices = [(1, '测试')]
    return render_template("学生信息页面.html", form=form)


@app.route("/testCheck/<int:page_id>")
def testCheck(page_id):
    return render_template("试卷复查页面.html", methods=['GET', 'POST'])


@app.route("/testCreater")
def testCreater():
    return render_template("教师创建考试页面.html", methods=['GET', 'POST'])


@app.route("/testList")
def testList():
    return render_template("教师考试计划页面.html", methods=['GET', 'POST'])


@app.route("/login", methods=['POST'])
def login():
    print(request.form['id'])
    form = LoginForm(request.form)
    if form.validate_on_submit():
        if form.role.data == 1:
            return redirect("studentMenu")
        elif form.role.data == 2:
            return redirect("teacherMenu")
        else:
            return redirect("adminMenu")
    else:
        return render_template("登录页面.html", form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    return redirect("index")


@app.route("/teacherRegister", methods=['GET', 'POST'])
def teacherRegister():
    return redirect("index")


@app.route("/studentRegister", methods=['GET', 'POST'])
def studentRegister():
    return redirect("index")


@app.route("/teacherInfoUpdate", methods=['GET', 'POST'])
def teacherInfoUpdate():
    return redirect("teacherInfo")


@app.route("/studentInfoUpdate", methods=['GET', 'POST'])
def studentInfoUpdate():
    return redirect("studentInfo")


@app.route("/collegeChecked/<int:college_id>", methods=['GET', 'POST'])
def collegeChecked():
    majors = [{'id': 1, 'name': "专"}, {'id': 2, 'name': "业"}]
    return majors
