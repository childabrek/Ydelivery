# flask
import os

from flask import Flask, render_template, redirect, request
from flask import abort, session, url_for, make_response
# flask_login
from flask_login import LoginManager, login_user, login_required
from flask_login import logout_user, current_user
# forms
from forms.user import RegisterForm, LoginForm
from forms.news import NewsForm
from forms.blank_post import BlankForm
# data
from data import db_session
from data.pizza import Pizza
from data.users import User
from data.drinks import Drinks
from data.combo import Combo
from data.blank_posts import Blank
from data.cart import Cart
import maps
import cart_p

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # форма авторизации
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
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    pizza = db_sess.query(Pizza)
    return render_template("index.html", news=pizza)


@app.route("/drinks")
def drink():
    db_sess = db_session.create_session()
    drinks = db_sess.query(Drinks)
    return render_template("drink.html", dri=drinks)


@app.route('/your_account', methods=['GET'])
@login_required
def account():
    db_sess = db_session.create_session()
    # получение ID текущего пользователя
    for i in db_sess.query(User).filter(User.id == int(current_user.get_id())):
        us = i
    return render_template('account.html', us=us)


@app.route('/delete-cookie/<int:valid>')
def delete_cookie(valid):
    # сохраняем и удаляем
    a = str(request.cookies.get('menu_pos', 0))
    a = a.replace(f' {valid}', '', 1).replace(' ', '!')
    res = make_response(redirect(f'/delete_cookie1/{a}/{valid}'))
    res.set_cookie('menu_pos', max_age=0)
    return res


@app.route('/delete_cookie1/<valid>/<b>')
def delete_cookie1(valid, b):
    valid = valid.replace(f'{b}', '', 1).replace('!', ' ').lstrip()
    res = make_response(redirect('/cart'))
    res.set_cookie('menu_pos', valid, 60 * 60 * 24 * 15)
    return res


@app.route('/cart/<int:idt>', methods=['GET', 'POST'])
@login_required
def add_pos(idt):
    db_sess = db_session.create_session()
    id_position = str(idt)[1::]
    id_menu = str(idt)[0]
    # индекс значения выбора таблицы
    if int(id_menu) == 1:
        for i in db_sess.query(Pizza).filter(Pizza.id == int(id_position)):
            posit = str(1) + str(i.id)
        res = make_response(redirect('/'))
    elif int(id_menu) == 2:
        for i in db_sess.query(Drinks).filter(Drinks.id == int(id_position)):
            posit = str(2) + str(i.id)
        res = make_response(redirect('/drinks'))
    elif int(id_menu) == 3:
        for i in db_sess.query(Combo).filter(Combo.id == int(id_position)):
            posit = str(3) + str(i.id)
        res = make_response(redirect('/combo'))
    else:
        abort(404)
    a = request.cookies.get('menu_pos', 0)

    if not a:
        res.set_cookie('menu_pos', str(posit), 60 * 60 * 24 * 15)
    else:
        res.set_cookie('menu_pos', str(a) + ' ' + str(posit), 60 * 60 * 24 * 15)
    return res


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart_v():
    a = cart_p.CartPost()
    result = a.cart_po()
    sum1 = a.sum_p()
    return render_template('cart.html', cart=result, summ=sum1)


@app.route('/image/<name>')
def image(name):
    db_sess = db_session.create_session()
    a = 'Стерлитамак'

    for i in db_sess.query(Blank).filter(Blank.name == name):
        a = a + ' ' + str(i.street) + ' ' + str(i.house)
        break
    ymap = maps.Maps(a)
    img = ymap.get_image()
    dist = round(ymap.get_distance(), 1)

    if dist <= 5:
        cost = 100
    elif dist <= 10:
        cost = 200

    return render_template('image.html', img=img, dist=dist, cost=cost)


@app.route('/blankp', methods=['GET', 'POST'])
def blank_post():
    form = BlankForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name != form.name.data).first():
            return render_template('blank.html', form=form,
                                   message='Такого пользователя не существует')
        a = cart_p.CartPost()
        struct = a.cart_po()
        for i in struct:
            answer = str(i.title), str(i.price)
            print(i.title, i.price)
        posts = Blank(
            name=form.name.data,
            street=form.street.data,
            structure=str(answer),
            house=form.house.data,
            flat=form.flat.data,
            phone=form.phone.data
        )
        db_sess.add(posts)
        db_sess.commit()
        return redirect(f'/image/{form.name.data}')
    return render_template('blank.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
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


if __name__ == '__main__':
    main()
