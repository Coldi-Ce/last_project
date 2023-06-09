from flask import Flask, render_template, redirect, make_response, request, session, abort

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.Codes import Codes
from data.users import User
from data.Topic import Topic
import datetime

from forms.code import CodeForm
from forms.mark import MarkForm
from forms.user import RegisterForm, LoginForm

from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def c():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = 0
    return render_template("main.html", user_id=user_id, title="Главная")


@app.route("/codes")
def code():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        codes = db_sess.query(Codes).filter(
            (Codes.user == current_user) | (Codes.is_private != True))
        user_id = current_user.id
    else:
        codes = db_sess.query(Codes).filter(Codes.is_private != True)
        user_id = 0
    return render_template("code.html", codes=codes, title="Выставка", user_id=user_id)


@app.route("/topics")
def topics():
    db_sess = db_session.create_session()
    topics = db_sess.query(Topic).filter()
    return render_template("topics.html", topics=topics)


@app.route('/codes/<int:id>', methods=['GET', 'POST'])
def coded(id):
    db_sess = db_session.create_session()
    code = db_sess.query(Codes).filter(Codes.id == id).first()
    if not code:
        return redirect('/codes')
    else:
        form = MarkForm()
        if form.validate_on_submit():
            code.mark += form.ma.data
            code.count += 1

        with open("co.py", "w") as myfile:
            myfile.write(code.script)
        if code.count != 0:
            avg = code.mark / code.count
        else:
            avg = 0
        return render_template('project.html', title=f'{code.title}', code=code, form=form, mark=avg)


@app.route('/user/<int:id>')
def us(id):
    db_sess = db_session.create_session()
    if current_user.is_authenticated and (db_sess.query(User).filter(User.id == id).first() == current_user):
        return render_template("user.html", user=db_sess.query(User).filter(User.id == id).first(),
                               title='Личный кабинет')
    return redirect('/')


@app.route('/topic/<int:id>')
def top(id):
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        codes = db_sess.query(Codes).filter(
            ((Codes.user == current_user) | (Codes.is_private != True)) and Codes.topic.id == id)
    else:
        codes = db_sess.query(Codes).filter((Codes.is_private != True) and Codes.topic.id == id)
    return render_template("code.html", codes=codes)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/create_codes', methods=['GET', 'POST'])
@login_required
def crc():
    form = CodeForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        to = db_sess.query(Topic).filter(Topic.name == form.top.data).first()
        if to:
            coode = Codes()
            coode.script = form.script.data
            coode.title = form.name.data
            coode.information = form.info.data
            to.codes.append(coode)
            coode.user = current_user
            db_sess.add(coode)
            db_sess.merge(to)
            db_sess.commit()
            return redirect('/')
        else:
            to = Topic()
            to.name = form.top.data
            db_sess.add(to)
            coode = Codes()
            coode.information = form.info.data
            coode.script = form.script.data
            coode.title = form.name.data
            to.codes.append(coode)
            coode.user = current_user
            db_sess.add(coode)
            db_sess.merge(to)
            db_sess.commit()
            return redirect('/')

    return render_template('news.html', title='Добавление новости', form=form)


def main():
    db_session.global_init("db/frprgrms.db")
    app.run(host="127.0.0.1", port=8080, debug=True)


if __name__ == '__main__':
    main()