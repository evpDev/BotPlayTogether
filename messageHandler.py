import vkapi
import random
from listGames import games, twtch
myGroupId = 147802225
def get_answer(body):
    message = "Привет, для какой игры хочешь найти тиммейта?"
    return message

def filterByGame(nameGame, user_id):#127955715
    resp = vkapi.api.groups.getMembers(group_id = 147802225, fields = ['status'])['users']
    # resp2 = [vkapi.api.board.getComments(group_id = 147802225, topic_id = 35489751)['items'][i]['text'] for i in range(1,vkapi.api.board.getComments(group_id = 147802225, topic_id = 35489751)['count'])]
    resp2 = vkapi.api.board.getComments(group_id = 147802225, topic_id = 35489751)['items']
    hums = []
    findGame = [name for game in games if game[0] == nameGame for name in game]
    for hum in resp:
        if (hum['id'] == user_id): continue
        endBracket = str(hum['status']).find(']')
        if endBracket > -1 and str(hum['status'])[1:endBracket] in findGame:
            online = 'online' if vkapi.api.users.get(user_ids = hum['id'], fields = ['online'])[0]['online'] else 'offline'
            hums.append([str(hum['id']),str(hum['last_name']),str(hum['first_name']),str(hum['status'])[endBracket+1:], online])
    for hum in resp2:
        if (hum['from_id'] == user_id): continue
        endBracket = str(hum['text']).find(']')
        strtext = str(hum['text']).lower()
        if endBracket > -1 and strtext[1:endBracket] in findGame:
            last_name = vkapi.api.users.get(user_ids = hum['from_id'])[0]['last_name']
            first_name = vkapi.api.users.get(user_ids = hum['from_id'])[0]['first_name']
            online = 'online' if vkapi.api.users.get(user_ids = hum['from_id'], fields = ['online'])[0]['online'] else 'offline'
            hums.append([str(hum['from_id']),last_name,first_name,str(hum['text'])[endBracket+1:], online])
    return hums


def create_answer(data, token):
    user_id = data['user_id']
    message = 'Вы ввели неверную комманду.\nВведите help, чтобы узнать доступные комманды'
    usersRequest = data['body'].lower().split(' ')
    if (usersRequest[0] == 'play'):
        people_search(usersRequest[1], token, user_id)
    elif (usersRequest[0] == 'help'):
        help_information(token, user_id)
    elif (usersRequest[0] == 'twitch'):
        get_video_twitch(usersRequest[1], token, user_id)
    else: vkapi.send_message(user_id, token, message)


def people_search(usersGame, token, user_id):
    message = 'Вы ввели неизвестную игру, сообщите об этом разработчикам'
    for game in games:
        for thisName in game:
            if thisName == usersGame:
                nameGame = game[0]
                message = ('Нет людей, готовых сейчас сыграть с Вами3(\nВведите название другой игры или подождите, ' +
                          'оставив в своём статусе заявку в формате:\n[Название игры]дополнительные сведения')
                resp = filterByGame(nameGame, user_id)
                # message = str(vkapi.api.users.get(user_ids = 167542207, fields = ['online'])[0]['online'])
                if resp: message = 'Вот люди, которые готовы сыграть:\n'
                for hum in resp:
                    # mystr = ', '.join([[hum['id'], hum['first_name'], hum['last_name'], hum['status']])
                    # message = message + "https://vk.com/id" + str(hum['id']) + ' , ' + str(hum['first_name']) + ' ' + str(hum['last_name']) + ': ' + str(hum['status']) + "\n"
                    message = message + "https://vk.com/id" + hum[0] + ' , ' + hum[1] + ' ' + hum[2] + '('+ hum[4] +'): ' + hum[3] + "\n"
    # message = get_answer(data['body'].lower())
    vkapi.send_message(user_id, token, message)

def help_information(token, user_id):
    message = ('twitch [название игры] - присылает видео с твича по данной игре\n'+
               'play [название игры] - ищет людей для совместной игры')
    vkapi.send_message(user_id, token, message)

def get_video_twitch(nameGame, token, user_id):
    # max_num = vkapi.api.video.get(owner_id = -147802225)['count']
    # num = 0
    # resp2 = vkapi.api.video.get(owner_id = str(-147802225))
    message = "К сожалению, по этой игре ещё нет ни одного видео. Обратитесь к разработчикам"
    if (twtch.get(nameGame) != None):
        attachment = 'video' + str(-myGroupId) + '_' + str(twtch[nameGame][random.randint(0, len(twtch[nameGame])-1)])
        message = "Вот случайное видео с твитча по игре " + nameGame# + " " + str(twtch[nameGame][random.randint(0, len(twtch[nameGame])-1)])

    # attachment = 'video' + str(-myGroupId) + '_' + str(456239021)
    vkapi.send_message(user_id, token, message, attachment)