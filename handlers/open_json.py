import json

def read_json_data():
    with open('data.json', mode = 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data
    

def write_register_json_data(login, password):
    data = read_json_data()
    
    new_data = {
    login : {
        'password' : password,
        'orders' : {'7712' : {'item_name' : 'Навушники Sony WH xb910n',
                                'item_id' : '1532',
                                'arrival_time' : '16.07.2023',
                                'price' : 8000,
                                'delivery_price' : 100},

                    '5466' : {'item_name' : 'Kingston SSDNow A400 480GB 2.5" SATAIII 3D V-NAND (SA400S37/480G)',
                                'item_id' : '3214',
                                'arrival_time' : '17.07.2023',
                                'price' : 1099,
                                'delivery_price' : 0}}
    }
}
    with open('data.json', mode = 'w', encoding='utf-8') as file:
        data.update(new_data)
        json.dump(data, file, indent = 4)

def write_json_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent= 4)
        

def check_login_and_password(login, password):
    data = read_json_data()

    if login in data:
        if data[str(login)]['password'] == password:
            return True
        

def check_if_logined(user_id):
    data = read_json_data()

    if str(user_id) in data['logined tg users']:
        return True
    else:
        return False
    

def get_login(id):
    data = read_json_data()
    login = data['logined tg users'][str(id)]

    return login
    

def get_orders_data(login):
    data = read_json_data()
    orders = data[login]['orders']
    return orders


def get_orders_msg(user_id):
        
    if check_if_logined(user_id):
        login = get_login(user_id)
    
    else:
        is_logined = False
        return is_logined


    orders = get_orders_data(login)
    msg = 'Виберіть ваще замовлення, інформацію про якого ви хочете отримати.\nВаші замовлення:\n'
    num = 1

    for order_data in orders.values():
        
        item_name = order_data['item_name'] 
        msg += f'{num}) {item_name}\n'
        num += 1

    return msg, orders
