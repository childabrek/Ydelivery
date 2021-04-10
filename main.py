from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import RegisterForm, LoginForm
from forms.news import NewsForm
from data import db_session
from data.pizza import Pizza
from data.users import User


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
    app.run()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    #     форма авторизации
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


# @app.route('/news', methods=['GET', 'POST'])
# @login_required
# def add_news():
#     form = NewsForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         news = Pizza()
#         news.title = form.title.data
#         news.content = form.content.data
#         news.is_private = form.is_private.data
#         current_user.news.append(news)
#         db_sess.merge(current_user)
#         db_sess.commit()
#         return redirect('/')
#     return render_template('works.html', title='Добавление работы',
#                            form=form)


# @app.route('/news/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_news(id):
#     form = NewsForm()
#     if request.method == "GET":
#         db_sess = db_session.create_session()
#         news = db_sess.query(Pizza).filter(Pizza.id == id,
#                                            Pizza.user == current_user
#                                            ).first()
#         if news:
#             form.title.data = news.title
#             form.content.data = news.content
#             form.is_private.data = news.is_private
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         news = db_sess.query(Pizza).filter(Pizza.id == id,
#                                            Pizza.user == current_user
#                                            ).first()
#         if news:
#             news.title = form.title.data
#             news.content = form.content.data
#             news.is_private = form.is_private.data
#             db_sess.commit()
#             return redirect('/')
#         else:
#             abort(404)
#     return render_template('news.html',
#                            title='Редактирование новости',
#                            form=form
#                            )
#
#
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
