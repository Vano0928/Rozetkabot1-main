import json

def read_json_data():
    with open('data.json', mode = 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data
    

def write_register_json_data(login, password):
    data = read_json_data()
    with open('data.json', mode = 'w', encoding='utf-8') as file:
        data.update({
            login : {
                'password' : password,
                'orders' : '[]',
                'logined tg accounts' : []
            }
        })
        json.dump(data, file, indent = 2)