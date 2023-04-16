from flask import Flask, render_template, redirect, make_response, request, session, abort

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.Codes import Codes
from data.users import User
from data.Topic import Topic
import datetime

from forms.code import CodeForm
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
    return render_template("main.html", title="Главная")


@app.route("/codes")
def code():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        codes = db_sess.query(Codes).filter(
            (Codes.user == current_user) | (Codes.is_private != True))
    else:
        codes = db_sess.query(Codes).filter(Codes.is_private != True)
    return render_template("code.html", codes=codes, title="Выставка")


@app.route("/topics")
def topics():
    db_sess = db_session.create_session()
    topics = db_sess.query(Topic).filter()
    return render_template("topics.html", topics=topics)


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


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


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


@app.route('/codes/<int:id>', methods=['GET', 'POST'])
def ed_wt(id):
    db_sess = db_session.create_session()
    code = db_sess.query(Codes).filter(Codes.id == id).first()
    with open("code.py", "w") as myfile:
        myfile.write(code.script)

    return render_template('.html', title=f'код{id}')



@app.route('/create/code', methods=['GET', 'POST'])
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
            coode.topic = to
            current_user.codes.append(coode)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')
        else:
            to = Topic()
            to.name = form.top.data
            coode = Codes()
            coode.information = form.info.data
            coode.script = form.script.data
            coode.title = form.name.data
            coode.topic = to
            current_user.codes.append(coode)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')

    return render_template('news.html', title='Добавление новости',
                            form=form)




def main():
    db_session.global_init("db/frprgrms.db")
    app.run(host="127.0.0.1", port=8080, debug=True)


if __name__ == '__main__':
    main()