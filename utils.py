import json
from datetime import datetime

def read_json(filename):
    with open(filename, "r", encoding='utf-8') as f:
        file = f.read()
        if file:
            file_json = json.loads(file)
            return file_json
        return []


def write_json():
    books = read_books_json()
    new_book['id'] = new_id(books)
    new_book['isbn'] = new_isbn(books)
    books.append(new_book)
    with open('books.json', 'w', encoding='utf-8', ) as f:
        json.dump(books, f, ensure_ascii=False, indent='\t')
    return books

def init_base(User, Order, Offer):
    raw_json = read_json('init.json')
    users = raw_json['users_data']
    orders = raw_json['orders_data']
    offers = raw_json['offers_data']
    init_db=[]
    if users:
        for user in users:
            init_db.append(User(id=user["id"],
                                  first_name=user["first_name"],
                                  last_name=user["last_name"],
                                  age=user["age"],
                                  email=user["email"],
                                  role=user["role"],
                                  phone=user["phone"]
                                  ))
    if orders:
        for order in orders:
            init_db.append(Order(id=order["id"],
                                     name=order["name"],
                                     description=order["description"],
                                     start_date=datetime.strptime(order["start_date"].replace("/", "-"),"%m-%d-%Y"),
                                     end_date=datetime.strptime(order["end_date"].replace("/", "-"),"%m-%d-%Y"),
                                     address=order["address"],
                                     price=order["price"],
                                     customer_id=order["customer_id"],
                                     executor_id=order["executor_id"]
                                     ))
    if offers:
        for offer in offers:
            init_db.append(Offer(id=offer["id"],
                                 order_id=offer["order_id"],
                                 executor_id=offer["executor_id"]
                                 ))
    return init_db