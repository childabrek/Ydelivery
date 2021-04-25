# flask
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
from data.cart import Cart

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
    # db_sess = db_session.create_session()
    # for p in db_sess.query(Pizza).all():
    #     print(p)
    # app.register_blueprint(jobs_api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


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
    # if current_user.is_authenticated:
    #     pizza = db_sess.query(Pizza).filter(
    #         (Pizza.user == current_user) | (Pizza.is_private != True))
    # else:
    #     pizza = db_sess.query(Pizza).filter(Pizza.is_private != True)
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
    # индекс значения выбора таблицы
    # if int(id_menu) == 1:
    #     for i in db_sess.query(Pizza).filter(Pizza.id == int(id_position)):
    #         posit = str(1) + str(i.id)
    #     res = make_response(redirect('/'))
    # elif int(id_menu) == 2:
    #     for i in db_sess.query(Drinks).filter(Drinks.id == int(id_position)):
    #         posit = str(2) + str(i.id)
    #     res = make_response(redirect('/drinks'))
    # elif int(id_menu) == 3:
    #     for i in db_sess.query(Combo).filter(Combo.id == int(id_position)):
    #         posit = str(3) + str(i.id)
    #     res = make_response(redirect('/combo'))
    # else:
    #     abort(404)
    a = str(request.cookies.get('menu_pos', 0))
    a = a.replace(f' {valid}', '', 1).replace(' ', '!')
    res = make_response(redirect(f'/delete_cookie1/{a}/{valid}'))
    res.set_cookie('menu_pos', max_age=0)
    # if not a:
    #     res.set_cookie('menu_pos', str(posit), 60 * 60 * 24 * 15)
    # else:
    #     res.set_cookie('menu_pos', str(a) + ' ' + str(posit), 60 * 60 * 24 * 15)
    return res


@app.route('/delete_cookie1/<valid>/<b>')
def delete_cookie1(valid, b):
    print(valid)
    valid = valid.replace(f'{b}', '', 1).replace('!', ' ')
    print(valid)
    res = make_response(redirect('/cart'))
    res.set_cookie('menu_pos', valid, 60 * 60 * 24 * 15)
    return res


@app.route('/cart/<int:idt>', methods=['GET', 'POST'])
@login_required
def add_pos(idt):
    db_sess = db_session.create_session()
    id_position = str(idt)[1::]
    id_menu = str(idt)[0]
    print('!!!!!!!!!!', id_menu)
    print('!!!!!!!!!!', id_position)
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
    db_sess = db_session.create_session()
    a = str(request.cookies.get('menu_pos', 0)).split()
    d = []
    sum1 = 0
    print(a)
    for j in a:
        if int(j[0]) == 1:
            for i in db_sess.query(Pizza).filter(Pizza.id == j[1]):
                i.id = int('1' + str(i.id))
                d.append(i)
                sum1 += i.price
        elif int(j[0]) == 2:
            for i in db_sess.query(Drinks).filter(Drinks.id == j[1]):
                i.id = int('2' + str(i.id))
                d.append(i)
                sum1 += i.price
        elif int(j[0]) == 3:
            for i in db_sess.query(Combo).filter(Combo.id == j[1]):
                i.id = int('3' + str(i.id))
                d.append(i)
                sum1 += i.price
        else:
            abort(404)
    print(d)
    print(sum1)
    return render_template('cart.html', cart=d, summ=sum1)


@app.route('/blankp', methods=['GET', 'POST'])
def blank_post():
    form = BlankForm()
    if form.validate_on_submit():
        return redirect('/cart')
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

# @app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def news_delete(id):
#     db_sess = db_session.create_session()
#     news = db_sess.query(Pizza).filter(Pizza.id == id,
#                                        Pizza.user == current_user
#                                        ).first()
#     if news:
#         db_sess.delete(news)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/')
