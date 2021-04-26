from flask import request
from flask import abort

from data import db_session
from data.combo import Combo
from data.drinks import Drinks
from data.pizza import Pizza


class CartPost:
    def __init__(self):
        self.a = str(request.cookies.get('menu_pos', 0)).split()
        self.sum1 = 0

    def cart_po(self):
        db_sess = db_session.create_session()
        d = []
        sum1 = 0
        for j in self.a:
            print(j)
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
        db_sess.close()
        self.sum1 = sum1
        return d

    def sum_p(self):
        return self.sum1
