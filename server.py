import random
import time

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from PIL import Image, ImageDraw, ImageFont

FILE1 = r'C:\Users\USER\PycharmProjects\Bot\easy.txt'
FILE2 = r'C:\Users\USER\PycharmProjects\Bot\moderate.txt'
FILE3 = r'C:\Users\USER\PycharmProjects\Bot\hard.txt'
FILE4 = r'C:\Users\USER\PycharmProjects\Bot\english.txt'
WORD = r'C:\Users\USER\PycharmProjects\Bot\result.png'
class BaseBot:
    def __init__(self, token: str):
        self._vk = vk_api.VkApi(token=token)
        self.__long_poll = VkLongPoll(self._vk)
        self.keyboard = KeyboardMixin()

    def start(self, commands):
        self.__commands = commands
        print('Игровой бот запущен. Чтобы начать, напишите "Начать".')
        for event in self.__long_poll.listen():
            print(event)
            print(event.type)
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    self._command_starter(event)

    def _command_starter(self, event):
        msg = event.text
        if self.__commands.get(msg.lower()):
            self.__commands[msg.lower()](event)
        else:
            self.command_name(event)

    def _send_msg(self, id: int, message: str, keyboard: VkKeyboard = None):
        if not keyboard:
            data = {
                'user_id': id,
                'message': message,
                'random_id': random.randint(1, 1000),

            }
            self._vk.method('messages.send', data)
        elif keyboard:
            data = {
                'user_id': id,
                'message': message,
                'random_id': random.randint(1, 1000),
                'keyboard': keyboard.get_keyboard()
            }
            self._vk.method('messages.send', data)

    def _send_image(self, id: int, message: str, attachment, keyboard: VkKeyboard = None):
        if not keyboard:
            data = {
                'user_id': id,
                'message': message,
                'attachment': attachment,
                'random_id': random.randint(1, 1000),

            }
            self._vk.method('messages.send', data)
        elif keyboard:
            data = {
                'user_id': id,
                'message': message,
                'attachment': attachment,
                'random_id': random.randint(1, 1000),
                'keyboard': keyboard.get_keyboard()
            }
            self._vk.method('messages.send', data)



    def send_empty_keyboard(self, event, message_txt):
        keyboard = VkKeyboard()
        keyboard.add_button(label='Начать игру', color=VkKeyboardColor.POSITIVE)
        self._vk.method("messages.send", {"user_id": event.user_id,
                                    "message": message_txt,
                                    "random_id": 0,
                                    "keyboard": keyboard.get_empty_keyboard(),
                                    })

    def command_name(self, event):
        pass

class Bot(BaseBot):
    users = {}
    commands_score = {}
    def __init__(self, *args, **kwargs):
        self.TheGame = TheGame(self)
        super().__init__(*args, **kwargs)
    def greeting(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Начать игру', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Правила', color=VkKeyboardColor.PRIMARY)
        self._send_msg(user_id,
                       'Привет, ты можешь прочитать правила или начать игру.', keyboard)
    

    def rules(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Начать игру', color=VkKeyboardColor.POSITIVE)
        self._send_msg(user_id,
                       'Правила игры таковы:... Если ты готов играть, напиши: "Игра".', keyboard)
        
    def prestart(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='2', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='3', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label='4', color=VkKeyboardColor.POSITIVE)
        self._send_msg(user_id,
                       'Сколько команд будет играть? Напиши цифру от 2 до 4.', keyboard)

    def command_amount(self, event):
        user_id = event.user_id
        if 1 < int(event.text) < 5:
            self.users[user_id] = {
                'command_amount': int(event.text),
                'command_name': [],
            }
            self.send_empty_keyboard(event, 'Введите название команды №1: ')

        else:
            self._send_msg(user_id,
                           'Количество команд от 2 до 4. Напиши цифру от 2 до 4.')
        
    def command_name(self, event):
        user_id = event.user_id
        if self.users.get(user_id):
            if len(self.users.get(user_id)['command_name']) != self.users.get(user_id)['command_amount']:
                self.users[user_id]['command_name'].append(event.text)
                if len(self.users.get(user_id)['command_name']) + 1 <= self.users.get(user_id)['command_amount']:
                    self._send_msg(user_id,
                                f"Введите название команды №{len(self.users.get(user_id)['command_name']) + 1}: ")
                else:
                    for i in self.users[user_id]['command_name']:
                        self.commands_score[i] = 0
                    self.victory_score(event)
        else:
            self._send_msg(user_id, 'Ваш ответ не распознан')

    def victory_score(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='25', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='50', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label='100', color=VkKeyboardColor.NEGATIVE)
        self._send_msg(user_id,
                       "До скольки очков играем для победы? Напиши: 25, 50 или 100.", keyboard)

    def set_victory_score(self, event):
        user_id = event.user_id
        if int(event.text) in [25, 50, 100]:
            self.users[user_id]['score'] = int(event.text)
            print(self.users)
            self.penalty(event)
        else:
            self._send_msg(user_id,
                           "Напиши: 25, 50 или 100.")
            self.set_victory_score(event)

    def penalty(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='да', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button(label='нет', color=VkKeyboardColor.POSITIVE)
        self._send_msg(user_id,
                       'Отнимать ли очки за пропуск слова?', keyboard)

    def set_penalty(self, event):
        user_id = event.user_id
        if event.text.lower() == 'да':
            self.users[user_id]['penalty'] = True
            self.explain_time(event)
        elif event.text.lower() == 'нет':
            self.users[user_id]['penalty'] = False
            self.explain_time(event)
        print(self.users)

    def explain_time(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='10', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='90', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label='120', color=VkKeyboardColor.NEGATIVE)
        self._send_msg(user_id,
                       'Сколько времени даём на объяснение?', keyboard)
    def set_explain_time(self, event):
        user_id = event.user_id
        if event.text.lower() == '10':
            self.users[user_id]['explain_time'] = int(event.text)
            self.choose_dict(event)
        elif event.text.lower() == '90':
            self.users[user_id]['explain_time'] = int(event.text)
            self.choose_dict(event)
        elif event.text.lower() == '120':
            self.users[user_id]['explain_time'] = int(event.text)
            self.choose_dict(event)
        print(self.users)

    def choose_dict(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Простой', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button(label='Средний', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Сложный', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label='Английский', color=VkKeyboardColor.NEGATIVE)
        self._send_msg(user_id,
                       'Выбери словарь для игры.', keyboard)


    def create_dict(self, event):
        user_id = event.user_id
        if event.text.lower() == 'простой':
            self.users = Dictionaries(event, self.users).create_easy_dict()
            self.TheGame.game_starter(event,)

        elif event.text.lower() == 'средний':
            self.users = Dictionaries(event, self.users).create_moderate_dict()
            self.TheGame.game_starter(event,)

        elif event.text.lower() == 'сложный':
            self.users = Dictionaries(event, self.users).create_hard_dict()
            self.TheGame.game_starter(event,)

        elif event.text.lower() == 'английский':
            self.users = Dictionaries(event, self.users).create_english_dict()
            self.TheGame.game_starter(event,)

        print(self.users)



class Dictionaries():
    def __init__(self, event, users):
        self.user_id = event.user_id
        self.users = users
    def create_easy_dict(self):
        with open(FILE1, encoding='utf-8') as f:
            easy = f.readlines()
            easy = [line.rstrip('\n') for line in easy]
            self.users[self.user_id]['dictionary'] = easy
            random.shuffle(self.users[self.user_id]['dictionary'])

            return self.users

    def create_moderate_dict(self):
        with open(FILE2, encoding='utf-8') as f:
            moderate = f.readlines()
            moderate = [line.rstrip('\n') for line in moderate]
            self.users[self.user_id]['dictionary'] = moderate
            return self.users

    def create_hard_dict(self):
        with open(FILE3, encoding='utf-8') as f:
            hard = f.readlines()
            hard = [line.rstrip('\n') for line in hard]
            self.users[self.user_id]['dictionary'] = hard
            return self.users

    def create_english_dict(self):
        with open(FILE4, encoding='utf-8') as f:
            english = f.readlines()
            english = [line.rstrip('\n') for line in english]
            self.users[self.user_id]['dictionary'] = english
            return self.users


class TheGame:
    def __init__(self, bot):
        self.bot = bot
        self.commands_counter = 0



    def game_starter(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Начать объяснение!', color=VkKeyboardColor.POSITIVE)
        self.zero_counter(event)
        self.active_command = self.bot.users[user_id]['command_name'][self.commands_counter]
        self.bot._send_msg(user_id,
                       f"Объясняет команда {self.active_command}", keyboard)

    def word_demonstration(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Следующее слово', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Пропустить слово', color=VkKeyboardColor.NEGATIVE)
        if self.bot.users[user_id]['words counter'] == 0:
            Time.time_start()
        else:
            self.score_counter(self.active_command)

        self.words_counter(event)
        if Time.time_check() == True:
            self.create_img(event)
            self.bot._send_image(user_id,
                                 {self.bot.users[user_id]['dictionary'][self.bot.users[user_id]['words counter']]},
                                 'WORD', keyboard)
            #self.bot._send_msg(user_id,
            #                   {self.bot.users[user_id]['dictionary'][self.bot.users[user_id]['words counter']]}, keyboard)
        else:
            self.finish_iteration(event)

    def create_img(self, event):
        user_id = event.user_id
        width = 250
        height = 250
        message = self.bot.users[user_id]['dictionary'][self.bot.users[user_id]['words counter']]
        font = ImageFont.truetype("arial.ttf", size=36)
        img = Image.new('RGB', (width, height), color='black')
        imgDraw = ImageDraw.Draw(img)
        textWidth, textHeight = imgDraw.textsize(message, font=font)
        xText = (width - textWidth) / 2
        yText = (height - textHeight) / 2
        imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 255))
        img.save('result.png')
        img.show()
    def zero_counter(self, event):
        user_id = event.user_id
        if not self.bot.users[user_id].get('words counter'):
            self.bot.users[user_id]['words counter'] = 0
        return self.bot.users[user_id]['words counter']

    def words_counter(self, event):
        user_id = event.user_id
        self.bot.users[user_id]['words counter'] += 1
        return self.bot.users[user_id]['words counter']



    def score_counter(self, command_title):
        self.bot.commands_score[command_title] += 1

    def commands_count(self, event):
        user_id = event.user_id
        self.commands_counter += 1
        if self.commands_counter >= self.bot.users.get(user_id)['command_amount']:
            self.commands_counter = 0

    def temp_score_counter(self, event):
        pass
    def finish_iteration(self, event):
        user_id = event.user_id
        self.bot._send_msg(user_id, "Время истекло!")
        print(self.bot.commands_score)
        self.commands_count(event)
        self.game_starter(event)



class Time(TheGame):
    def __init__(self, game):
        self.game = game

    def time_start(self):
        self.__time_start = time.perf_counter()

    def time_current(self):
        time_current = time.perf_counter()
        return time_current

    def time_check(self, event):
        user_id = event.user_id
        if self.time_current() - self.__time_start < self.bot.users[user_id]['explain_time']:
            return True
        else:
                return False

class KeyboardMixin(VkKeyboard):
    """
    Working with the VK keyboard, implemented methods for
    getting, hiding the keyboard and showing auxiliary commands
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def hide_keyboard(self, label: str = '📌️Вернуть клавиатуру'):
        keyboard = VkKeyboard()
        keyboard.add_button(label=label, color=VkKeyboardColor.POSITIVE)
        return keyboard

    def get_standart_keyboard(self):
        keyboard = VkKeyboard()
        keyboard.add_button(label='Начать игру', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Правила', color=VkKeyboardColor.PRIMARY)
        return keyboard

    def get_help(self):
        keyboard = VkKeyboard()
        keyboard.add_button(label='🔎Помощь', color=VkKeyboardColor.POSITIVE)
        return keyboard
