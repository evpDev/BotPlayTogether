
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, json
from settings import token, confirmation_token
# import vk
import messageHandler


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/', methods=['POST'])
def processing():
    #Распаковываем json из пришедшего GET-запроса
    data = json.loads(request.data)
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        # session = vk.Session()
        # api = vk.API(session, v=5.0)
        # user_id = data['object']['user_id']
        # api.messages.send(access_token=token, user_id=str(user_id), message='Привет, я новый бот!')
        messageHandler.create_answer(data['object'], token)
        # Сообщение о том, что обработка прошла успешно
        return 'ok'