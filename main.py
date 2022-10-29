import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = 'vk1.a.nxwYoT0jJ_yZA2EWa_JO5K_On6IkShsY71FkxuenlLNtqNime-lYvXs7gMleTIBKMdS31fj1tFC7KdT01_8WS7h8kHYDkBazzbcUtOTu52kI3jbPwsV5BmE7j6mF3a1fwc_ehAelhJVrgx1VcFxqoc_jbg1ZTgxlCfbU-dIUYqIzUj4pfAposuRnfq-brSQI7zrUVdty4R9JNXSE_MgTHg'

def send_msg(id, message):
    data = {
        'user_id': id,
        'message': message,
        'random_id': random.randint(1, 1000)
    }
    vk.method('messages.send', data)


vk = vk_api.VkApi(token=TOKEN)
long_poll = VkLongPoll(vk)
# long_poll = vk_api.longpoll.VkLongPoll(vk)
print('Я запущен. Ваш бот')

# for event in long_poll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#         if event.to_me:
#             if event.text.lower() == 'abc':
#                 send_msg(event.user_id, 'Мы делаем фаршированную рыбу и не надо сюда писать!')

#for event in long_poll.listen():
#    if event.type == VkEventType.MESSAGE_NEW:
#        if event.to_me:
#            if event.text.lower() == 'Игра':
#                send_msg(event.user_id, 'Давай поиграем в угадай число')

for event in long_poll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text.lower() == 'привет':
            send_msg(event.user_id, 'От старых штиблет!')
        elif event.text.lower() == 'здравствуйте':
            send_msg(event.user_id, 'И вам не хворать!')
        else:
            send_msg(event.user_id, 'Нипанятна!')
