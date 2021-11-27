from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import utils


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homework.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    def to_dict(self):
        return {"id":self.id,
                "first_name":self.first_name,
                "last_name":self.last_name,
                "age":self.age,
                "email":self.email,
                "role":self.role,
                "phone":self.phone
                }


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {"id":self.id ,
                "name":self.name ,
                "description":self.description ,
                "start_date":self.start_date ,
                "end_date":self.end_date ,
                "address":self.address ,
                "price":self.price ,
                "customer_id":self.customer_id ,
                "executor_id":self.executor_id}


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {"id":self.id,
                "order_id":self.order_id,
                "executor_id":self.executor_id
                }


db.drop_all()
db.create_all()
db.session.commit()
init_db = utils.init_base(User, Order, Offer)
db.session.add_all(init_db)
db.session.commit()


@app.route('/users', methods = ['GET', 'POST'])
def users():
    if request.method =='GET':
        response_users = []
        for user in db.session.query(User).all():
            response_users.append(user.to_dict())
        return jsonify(response_users)
    if request.method == 'POST':
        data = request.json
        try:
            user_to_add = User(**data)
            db.session.add(user_to_add)
            db.session.commit()
        except:
            return 'Ошибка добавления', 400
        return "User добавлен", 200


@app.route('/users/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def users_by_id(id:int):
    if request.method =='GET':
        response_users = []
        for user in db.session.query(User).filter(User.id==id).all():
            response_users.append(user.to_dict())
        return jsonify(response_users)
    if request.method == 'PUT':
        data = request.json
        if set(data.keys())==(set(User.metadata.tables['users'].columns.keys())):
            db.session.query(User).filter(User.id == id).update(data)
            db.session.commit()
            return "User изменен", 200
        return 'Ошибка изменения', 400
    if request.method == 'DELETE':
        try:
            user = db.session.query(User).get(id)
            db.session.delete(user)
            db.session.commit()
            return "User удален", 200
        except Exception as e:
            return f'Ошибка: "{e}"',404


@app.route('/orders', methods = ['GET', 'POST'])
def orders():
    if request.method == 'GET':
        response_orders = []
        orders = db.session.query(Order).all()
        if orders:
            for order in orders:
                response_orders.append(order.to_dict())
        return jsonify(response_orders)
    if request.method == 'POST':
        data = request.json
        try:
            order_to_add = Order(**data)
            db.session.add(order_to_add)
            db.session.commit()
        except:
            return 'Ошибка добавления', 400
        return "order добавлен", 200


@app.route('/orders/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def orders_by_id(id:int):
    if request.method == 'GET':
        response_orders = []
        for order in  db.session.query(Order).filter(Order.id==id).all():
            response_orders.append(order.to_dict())
        return jsonify(response_orders)
    if request.method == 'PUT':
        data = request.json
        if set(data.keys()) == (set(Offer.metadata.tables['orders'].columns.keys())):
            db.session.query(Order).filter(User.id == id).update(data)
            db.session.commit()
            return "Order изменен", 200
        return 'Ошибка изменения', 400
    if request.method == 'DELETE':
        try:
            order = db.session.query(Order).get(id)
            db.session.delete(order)
            db.session.commit()
            return "order удален", 200
        except Exception as e:
            return f'Ошибка: "{e}"',404


@app.route('/offers', methods = ['GET', 'POST'])
def offers():
    if request.method == 'GET':
        response_offers = []
        for offer in db.session.query(Offer).all():
            response_offers.append(offer.to_dict())
        return jsonify(response_offers)
    if request.method == 'POST':
        data = request.json
        try:
            offer_to_add = Offer(**data)
            db.session.add(offer_to_add)
            db.session.commit()
        except:
            return 'Ошибка добавления', 400
        return "offer добавлен", 200


@app.route('/offers/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def offers_by_id(id:int):
    if request.method == 'GET':
        response_offers = []
        for offer in db.session.query(Offer).filter(Offer.id==id).all():
            response_offers.append(offer.to_dict())
        return jsonify(response_offers)
    if request.method == 'PUT':
        data = request.json
        if set(data.keys()) == (set(Offer.metadata.tables['offers'].columns.keys())):
            db.session.query(Offer).filter(User.id == id).update(data)
            db.session.commit()
            return "Offer изменен", 200
        return 'Ошибка изменения', 400
    if request.method == 'DELETE':
        try:
            offer = db.session.query(Offer).get(id)
            db.session.delete(offer)
            db.session.commit()
            return "offer удален", 200
        except Exception as e:
            return f'Ошибка: "{e}"',404

if __name__ == "__main__":
    app.run(debug=True)