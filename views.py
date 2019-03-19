from flask import render_template, redirect, flash, url_for, request, json, session
from flask_login import login_required, current_user, LoginManager, login_user
from forms import LoginForm, RegisterFormStudent, RegisterFormTeacher, StudentInfoForm, TeacherInfoForm, TestCreaterForm
from models import app, Student, Teacher, College, Major, Subject, Plan, Page, Test, Class, TestType, db
from sqlalchemy.exc import IntegrityError, InternalError
import time


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate_on_submit():
            id = int(form.id.data)
            password = form.password.data
            if form.role.data == 1:
                user = Student.query.get(id)
                if user is None:
                    flash("学号输入错误！")
                elif user.checkPassword(password):
                    session["is_login"] = True
                    session["uid"] = user.id
                    session["role"] = "student"
                    return redirect("studentMenu")
                else:
                    flash("密码不正确！")
            elif form.role.data == 2:
                user = Teacher.query.get(id)
                if user is None:
                    flash("工号输入错误！")
                elif user.checkPassword(password):
                    session["is_login"] = True
                    session["uid"] = user.id
                    session["role"] = "teacher"
                    return redirect("teacherMenu")
                else:
                    flash("密码不正确！")
                    pass
                pass
            pass
        else:
            pass
    else:
        try:
            if session["is_login"]:
                flash("你已经登录，无需重复登录！")
                return redirect(session["role"] + "Menu")
        except Exception:
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


@app.route("/teacherInfo", methods=['GET', 'POST'])
def teacherInfo():
    form = TeacherInfoForm()
    return render_template("教师信息页面.html", form=form)


@app.route("/studentInfo", methods=['GET', 'POST'])
def studentInfo():
    form = StudentInfoForm()
    user = Student.query.get(session["uid"])
    if request.method == "GET":
        form.id.data = user.id
        form.name.data = user.name
        # 年级列表
        localtime = time.localtime(time.time())
        if localtime.tm_mon >= 9:
            first_grade = localtime.tm_year
        else:
            first_grade = localtime.tm_year - 1
        a = first_grade - user.grade
        grades = [user.grade+a, user.grade-1+a, user.grade-2+a, user.grade-3+a]
        del grades[a]
        form.grade.choices = [(user.grade, user.grade),
                              (grades[0], grades[0]),
                              (grades[1], grades[1]),
                              (grades[2], grades[2])]

        college = College.query.get(user.id_college)
        form.college.choices = [(college.id, college.name)]
        major = Major.query.get(user.id_major)
        form.major.choices = [(major.id, major.name)]
        classes = Class.query.get(user.id_class)
        form.classes.choices = [(classes.id, classes.name)]
        return render_template("学生信息页面.html", form=form)
    else:
        name = form.name.data
        id_college = form.college.data
        grade = form.grade.data
        id_class = form.classes.data
        id_major = form.major.data
        new_password = form.new_password.data
        pre_password = form.pre_password.data

        college = College.query.get(id_college)
        form.college.choices = [(id_college, college.name)]
        major = Major.query.get(id_major)
        form.major.choices = [(id_major, major.name)]
        classes = Class.query.get(id_class)
        form.classes.choices = [(id_class, classes.name)]
        form.grade.choices = [(grade, grade)]

        if user.checkPassword(pre_password):
            if form.new_password.data == form.ensure_password.data:
                # 改资料
                try:
                    user.name = name
                    user.id_college = id_college
                    user.grade = grade
                    user.id_class = id_class
                    user.id_major = id_major
                    db.session.commit()
                except InternalError:
                    db.session.rollback()
                    flash("信息不完善，请重新输入！")
                    return render_template('学生信息页面.html', form=form)
                #不为空，改新密码
                if new_password:
                    user.password = new_password
                    db.session.commit()
                    flash("修改成功！")
                    return redirect('/logout')
                #为空
                else:
                    pass
                flash("修改成功！")
                return redirect('studentInfo')
            else:
                flash("两次密码不一致！")
                return render_template('学生信息页面.html', form=form)
        else:
            flash("密码错误！")
            return render_template('学生信息页面.html', form=form)


@app.route("/testCheck/<int:page_id>")
def testCheck(page_id):
    return render_template("试卷复查页面.html", methods=['GET', 'POST'])


@app.route("/testCreater")
def testCreater():
    return render_template("教师创建考试页面.html", methods=['GET', 'POST'])


@app.route("/testList")
def testList():
    return render_template("教师考试计划页面.html", methods=['GET', 'POST'])


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("index")


# 浩：教师注册页面==================================================================================
@app.route("/teacherRegister", methods=['GET', 'POST'])
def teacherRegister():
    if request.method == 'GET':
        form = RegisterFormTeacher()
        return render_template('教师注册页面.html', form=form)
    else:
        form = RegisterFormTeacher(request.form)
        if form.validate_on_submit():
            user = Teacher()
            user.id = form.id.data
            user.name = form.name.data
            user.setPassword(form.password.data)
            if Teacher.query.get(user.id) is not None:
                flash("此工号已经被注册！！！！")
                return render_template('教师注册页面.html', form=form)
            db.session.add(user)
            db.session.commit()

            return redirect('index')
        else:
            flash("输入有误，请重新输入")
            return render_template('教师注册页面.html', form=form)


@app.route("/studentRegister", methods=['GET', 'POST'])
def studentRegister():
    if request.method == "POST":
        form = RegisterFormStudent(request.form)
        id = int(request.form.get("id"))
        name = request.form.get("name")
        college_id = request.form.get("college")
        grade = request.form.get("grade")
        classes_id = request.form.get("classes")
        major_id = request.form.get("major")
        password = request.form.get("password")
        ensure_password = request.form.get("ensure_password")
        user = Student(id=id, name=name, id_college=college_id, id_major=major_id, grade=grade, id_class=classes_id,
                       password=password)

        if password == ensure_password:
            try:
                db.session.add(user)
                db.session.commit()
                flash("注册成功！")
                pass
            except InternalError:
                db.session.rollback()
                flash("信息不完善，请重新输入！")
                return render_template('学生注册页面.html', form=form)
            except IntegrityError:
                db.session.rollback()
                flash("该学号已被其他用户注册，请联系管理员！")
                pass
            return redirect("/login")
            pass
        else:
            flash("两次密码不一致！")
            return redirect("/studentRegister")
            pass
    else:
        form = RegisterFormStudent()
        form.college.choices = [(1, '==wadada===')]
        form.major.choices = [(1, '请先选择学院')]
        localtime = time.localtime(time.time())
        if localtime.tm_mon >= 9:
            first_grade = localtime.tm_year
        else:
            first_grade = localtime.tm_year - 1
        form.grade.choices = [(first_grade - 3, first_grade - 3),
                              (first_grade - 2, first_grade - 2),
                              (first_grade - 1, first_grade - 1),
                              (first_grade, first_grade)]
        form.classes.choices = [(1, '请先选择专业')]
        return render_template("学生注册页面.html", form=form)


@app.route("/teacherInfoUpdate", methods=['GET', 'POST'])
def teacherInfoUpdate():
    return redirect("teacherInfo")


@app.route("/studentRegister/selects", methods=["POST"])
def studentRegisterSelects():
    print(request.form)
    data = {"data": []}
    if request.form['my_select'] == 'college':
        colleges = College.query.all()
        for college in colleges:
            data["data"].append({"id": college.id, "name": college.name})
        pass
    elif request.form['my_select'] == 'major':
        parent_id = request.form['parent_id']
        college = College.query.get(parent_id)
        for major in college.majors:
            data["data"].append({"id": major.id, "name": major.name})
        pass
    else:
        parent_id = request.form['parent_id']
        major = Major.query.get(parent_id)
        for clas in major.classes:
            data["data"].append({"id": clas.id, "name": clas.name})
        pass
    return json.dumps(data)
