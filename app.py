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
    age = db.Column(db.String)
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
    price = db.Column(db.String)
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
        users = db.session.query(User).all()
        if users:
            for user in users:
                response_users.append(user.to_dict())
        return jsonify(response_users)
    if request.method == 'POST':
        data = request.json
        if set(data.keys()).issubset(set(User.metadata.tables['users'].columns.keys())):
            user_to_add = User(first_name=data["first_name"],
                                last_name=data["last_name"],
                                age=data["age"],
                                email=data["email"],
                                role=data["role"],
                                phone=data["phone"]
                                )
            try:
                db.session.add(user_to_add)
                db.session.commit()
            except:
                return 'Ошибка добавления', 418
            return "User добавлен", 200
        return 'Unprocessable Entity', 422


@app.route('/users/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def users_by_id(id:int):
    if request.method =='GET':
        response_users = []
        users = db.session.query(User).filter(User.id==id).all()
        if users:
            for user in users:
                response_users.append(user.to_dict())
        return jsonify(response_users)
    if request.method == 'PUT':
        data = request.json
        if set(data.keys()).issubset(set(User.metadata.tables['users'].columns.keys())):
            user=db.session.query(User).get(id)
            user.first_name=data["first_name"]
            user.last_name=data["last_name"]
            user.age=data["age"]
            user.email=data["email"]
            user.role=data["role"]
            user.phone=data["phone"]
            try:
                db.session.add(user)
                db.session.commit()
            except:
                return 'Ошибка изменения', 418
            return "User изменен", 200
        return 'Unprocessable Entity', 422
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
        if set(data.keys()).issubset(set(Order.metadata.tables['orders'].columns.keys())):
            order_to_add = Order(name=data["name"],
                                 description=data["description"],
                                 start_date=datetime.strptime(data["start_date"].replace("/", "-"),"%m-%d-%Y"),
                                 end_date=datetime.strptime(data["end_date"].replace("/", "-"),"%m-%d-%Y"),
                                 address=data["address"],
                                 price=data["price"],
                                 customer_id=data["customer_id"],
                                 executor_id=data["executor_id"]
                                )
            try:
                db.session.add(order_to_add)
                db.session.commit()
            except:
                return 'Ошибка добавления', 418
            return "order добавлен", 200
        return 'Unprocessable Entity', 422

@app.route('/orders/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def orders_by_id(id:int):
    if request.method == 'GET':
        response_orders = []
        orders = db.session.query(Order).filter(Order.id==id).all()
        if orders:
            for order in orders:
                response_orders.append(order.to_dict())
        return jsonify(response_orders)
    if request.method == 'PUT':
        data = request.json
        if set(data.keys()).issubset(set(Order.metadata.tables['orders'].columns.keys())):
            order=db.session.query(Order).get(id)
            order.name=data["name"]
            order.description=data["description"]
            order.start_date=data["start_date"]
            order.end_date=data["end_date"]
            order.address=data["address"]
            order.price=data["price"]
            order.customer_id = data["customer_id"]
            order.executor_id = data["executor_id"]
            try:
                db.session.add(order)
                db.session.commit()
            except:
                return 'Ошибка изменения', 418
            return "order изменен", 200
        return 'Unprocessable Entity', 422
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
        offers = db.session.query(Offer).all()
        if offers:
            for offer in offers:
                response_offers.append(offer.to_dict())
        return jsonify(response_offers)
    if request.method == 'POST':
        data = request.json
        if set(data.keys()).issubset(set(Offer.metadata.tables['offers'].columns.keys())):
            offer_to_add = Offer(order_id=offer["order_id"],
                                 executor_id=offer["executor_id"]
                                )
            try:
                db.session.add(offer_to_add)
                db.session.commit()
            except:
                return 'Ошибка добавления', 418
            return "offer добавлен", 200
        return 'Unprocessable Entity', 422


@app.route('/offers/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def offers_by_id(id:int):
    if request.method == 'GET':
        response_offers = []
        offers = db.session.query(Offer).filter(Offer.id==id).all()
        if offers:
            for offer in offers:
                response_offers.append(offer.to_dict())
        return jsonify(response_offers)
    if request.method == 'PUT':
        data = request.json
        if set(data.keys()).issubset(set(Offer.metadata.tables['offers'].columns.keys())):
            offer=db.session.query(Offer).get(id)
            offer.order_id=data["order_id"]
            offer.executor_id=data["executor_id"]
            try:
                db.session.add(offer)
                db.session.commit()
            except:
                return 'Ошибка изменения', 418
            return "offer изменен", 200
        return 'Unprocessable Entity', 422
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