import random
import time

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType #Импортируем модуль для связи с пользователями (длинные запросы)
from vk_api.keyboard import VkKeyboard, VkKeyboardColor #Импортируем модуль для создания клавиатуры

# from PIL import Image, ImageDraw, ImageFont Пока изображения не используются

#Прописываем пути ко всем используемым файлам:
FILE1 = r'C:\Users\USER\PycharmProjects\Bot\easy.txt'
FILE2 = r'C:\Users\USER\PycharmProjects\Bot\moderate.txt'
FILE3 = r'C:\Users\USER\PycharmProjects\Bot\hard.txt'
FILE4 = r'C:\Users\USER\PycharmProjects\Bot\english.txt'
WORD = r'C:\Users\USER\PycharmProjects\Bot\result.png'

class BaseBot:
    """
    Устанавливаем все базовые параметры, связанные с VK.
    """
    def __init__(self, token: str):
        """
        Инициализируем базовые функции для VK API, а также создаем объект класса KeyboardMixin (описан в конце кода)
        :param token: Передаём токен из файла start.py
        """
        self._vk = vk_api.VkApi(token=token)
        self.__long_poll = VkLongPoll(self._vk) #Создаём объект класса VkLongPoll?
        self.keyboard = KeyboardMixin() #Используем или нет? Есть ощущение, что не используем.

    def start(self, commands):
        """
        Данный метод запускается в конце файла start.py. Выводит в консоль сообщение о корректной работе бота. Когда в
        диалоговом окне бота появится любое сообщение боту, запустит следующий метод _command_starter
        :param commands: Передаются из файла start.py, описаны в словаре COMMANDS
        :return:
        """
        self.__commands = commands
        print('Игровой бот запущен. Чтобы начать, напишите "Начать".')
        for event in self.__long_poll.listen():
            print(event)
            print(event.type)
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    self._command_starter(event)

    def _command_starter(self, event):
        """
        Создаёт переменную msg из текста переданного в метод eventа
        :param event:
        :return:
        """
        msg = event.text
        if self.__commands.get(msg.lower()):
            self.__commands[msg.lower()](event)
        else:
            self.command_name(event) #ссылается на пустой метод

    def _send_msg(self, id: int, message: str, keyboard: VkKeyboard = None):
        """
        Создаёт метод для отправки сообщений. Если параметр keyboard не упоминается, выведет сообщение без клавиатуры.
        Если в конце написать keyboard, появится клавиатуры (при помощи метода get_keyboard()
        :param id: id юзера ВКонтакте
        :param message: текст сообщения
        :param keyboard: наличие или отсутствие клавиатуры
        :return:
        """
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
        """
        Может отправлять картинку в виде вложения (attachment), по факту не используется в данный момент.
        :param id:
        :param message:
        :param attachment:
        :param keyboard:
        :return:
        """
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
        """
        Отправляет сообщение без клавиатуры при помощи метода get_empty_keyboard
        :param event:
        :param message_txt:
        :return:
        """
        keyboard = VkKeyboard()
        keyboard.add_button(label='Начать игру', color=VkKeyboardColor.POSITIVE)
        self._vk.method("messages.send", {"user_id": event.user_id,
                                    "message": message_txt,
                                    "random_id": 0,
                                    "keyboard": keyboard.get_empty_keyboard(),
                                    })

class Bot(BaseBot):
    """
    Класс Бот используется для предварительных настроек игры. В классе создается словарь users для учёта всего
    необходимого и словарь commands_score для учета очков команд.
    """
    users = {}
    commands_score = {}
    def __init__(self, *args, **kwargs):
        """
        Связывает данный класс с основным классом игры - TheGame
        :param args:
        :param kwargs:
        """
        self.TheGame = TheGame(self)
        super().__init__(*args, **kwargs)
    def greeting(self, event):
        """
        Выводится по команде "начать" из стартового файла (при открытии пользователем диалога с ботом)
        :param event:
        :return:
        """
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Начать игру', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Правила', color=VkKeyboardColor.PRIMARY)
        self._send_msg(user_id,
                       'Привет, ты можешь прочитать правила или начать игру.', keyboard)
    

    def rules(self, event):
        """
        Выводится по команде "Правила" из стартового файла.
        :param event:
        :return:
        """
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Начать игру', color=VkKeyboardColor.POSITIVE)
        self._send_msg(user_id,
                       'Правила игры: Каждая команда состоит из двух человек (возможно больше по желанию). Один человек'
                       'объясняет другому из своей команды слова, появляющиеся на экране. Запрещено использовать одно-'
                       'коренные слова, произносить отдельно любую букву слова, указывать на какие-либо предметы.'
                       'Если ты готов играть, жми "Начать игру".', keyboard)
        
    def get_command_amount(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='две', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='три', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label='четыре', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='пять', color=VkKeyboardColor.PRIMARY)
        self._send_msg(user_id,
                       'Сколько команд будет играть?', keyboard)

    def set_command_amount(self, event):
        user_id = event.user_id
        if event.text.lower() == 'две':
            self.users[user_id] = {
                'command_amount': 2,
                'command_name': [],
            }
            self.send_empty_keyboard(event, 'Введите название команды №1: ')
        elif event.text.lower() == 'три':
            self.users[user_id] = {
                'command_amount': 3,
                'command_name': [],
            }
            self.send_empty_keyboard(event, 'Введите название команды №1: ')
        elif event.text.lower() == 'четыре':
            self.users[user_id] = {
                'command_amount': 4,
                'command_name': [],
            }
            self.send_empty_keyboard(event, 'Введите название команды №1: ')
        elif event.text.lower() == 'пять':
            self.users[user_id] = {
                'command_amount': 5,
                'command_name': [],
            }
            self.send_empty_keyboard(event, 'Введите название команды №1: ')


        
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
        keyboard.add_button(label='5', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='50', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label='100', color=VkKeyboardColor.NEGATIVE)
        self._send_msg(user_id,
                       "До скольки очков играем для победы? Напиши: 25, 50 или 100.", keyboard)

    def set_victory_score(self, event):
        user_id = event.user_id
        if int(event.text) in [5, 50, 100]:
            self.users[user_id]['score'] = int(event.text)
            print(self.users)
            self.penalty(event)
        else:
            self._send_msg(user_id,
                           "Напиши: 5, 50 или 100.")
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
        keyboard.add_button(label='11', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='90', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label='120', color=VkKeyboardColor.NEGATIVE)
        self._send_msg(user_id,
                       'Сколько времени даём на объяснение?', keyboard)
    def set_explain_time(self, event):
        user_id = event.user_id
        if event.text.lower() == '11':
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
            self.TheGame.start_circle(event)

        elif event.text.lower() == 'средний':
            self.users = Dictionaries(event, self.users).create_moderate_dict()
            self.TheGame.start_circle(event)

        elif event.text.lower() == 'сложный':
            self.users = Dictionaries(event, self.users).create_hard_dict()
            self.TheGame.start_circle(event)

        elif event.text.lower() == 'английский':
            self.users = Dictionaries(event, self.users).create_english_dict()
            self.TheGame.start_circle(event)

        print(self.users)



class Dictionaries:
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
        self.words_counter = 0
        self.time = Time(bot)
        self.image = Images(bot)

    def start_circle(self, event):

        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Начать объяснение!', color=VkKeyboardColor.POSITIVE)
        self.commands_counter = 0
        self.active_command = self.bot.users[user_id]['command_name'][self.commands_counter]
        self.bot._send_msg(user_id,
                       f"Объясняет команда {self.active_command}", keyboard)

    def start_explanation(self, event):
        self.temporary_score_counter = 0
        self.time.time_start()
        self.temp_words_list = []
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Следующее слово', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Пропустить слово', color=VkKeyboardColor.NEGATIVE)
        self.bot._send_msg(user_id,
                           {self.bot.users[user_id]['dictionary'][self.words_counter]}, keyboard)

    def demonstrate_word(self, event):
        """
        Демонстрация слов (def demonstrate_word)
Вывести слово из списка по индексу words_counter
При нажатии «следующее слово»:
Прибавить единицу к временному счетчику очков (temporary_score_counter)
Проверить, не истекло ли время вызовом функции time_check (либо последовательным вызовом функции time_current time_check, либо вызов текущего времени запихнуть в time_check (лучше так)
Если время истекло (False), вывести «Время истекло» и вызвать функцию (def finish explanation)
Если время не истекло (True) вывести функцией саму себя
“””
Каждое показанное слово, после которого нажато «следующее слово» нужно заносить в отдельный временный список для демонстрации в конце хода. Temp_words_list = []
“””
При нажатии «пропустить слово»:
Если ранее было выбрано penalty: True - Отнять единицу от временного счетчика очков (если он уже больше нуля, иначе ничего не делать). Если penalty:False, очки не отнимаем.
Проверить, не истекло ли время вызовом функции time_check (либо последовательным вызовом функции time_current time_check, либо вызов текущего времени запихнуть в time_check (лучше так)
Если время истекло (False), вывести «Время истекло» и вызвать функцию (def finish explanation)
Если время не истекло (True) вывести функцией саму себя

        :param event:
        :return:
        """
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Следующее слово', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Пропустить слово', color=VkKeyboardColor.NEGATIVE)
        #    self.score_counter(self.active_command)
        if event.text.lower() == 'следующее слово':
            self.temporary_score_counter += 1
            self.temp_words_list.append(self.bot.users[user_id]['dictionary'][self.words_counter])
            print(self.temp_words_list)

        if event.text.lower() == 'пропустить слово':
            if self.bot.users[user_id]['penalty'] == True:
                self.temporary_score_counter -= 1
                if self.temporary_score_counter < 0:
                    self.temporary_score_counter = 0

        self.count_words(event)

        if self.time.time_check(event) == True:
            #self.create_img(event)
            #self.bot._send_image(user_id,
            #                     {self.bot.users[user_id]['dictionary'][self.bot.users[user_id]['words counter']]},
            #                     'WORD', keyboard)
            self.bot._send_msg(user_id,
                               {self.bot.users[user_id]['dictionary'][self.words_counter]}, keyboard)
        else:
            self.bot._send_msg(user_id,
                               'Время истекло!',
                               keyboard)
            self.finish_explanation(event)


    def finish_explanation(self, event):
        """
        Финиш хода (def finish explanation):
Вывести на экран слова, после которых было нажато «следующее слово» (temp_words_list[]) и спросить, сколько слов команда объяснила правильно (неправильно?)
Попросить подтвердить правильность данного количества засчитанных слов. (как?!, У нас идет пересечение с командами 2, 3, 4. Например, можно переписать кнопки количества команд на «одна» «две» «три» «четыре». Тогда вопрос «сколько слов команда объяснила неправильно. Принять введённый ответ текстом и отнять его из temporary_score_counter, при этом он не должен быть меньше нуля. Например, проверить, если в итоге значение стало меньше нуля, умножить его на ноль)
Положить значение из временного счетчика очков (temporary_score_counter) в список(словарь) очков каждой команды.
Показать значение из списка очков каждой команды (как?!)
Проверить, что счётчик команд по порядку (commands_counter) меньше количества команд. Если меньше, вызвать старт хода (def start_explanation) следующей команды (commands_counter += 1)
Если счётчик команд по порядку равен количеству команд, значит, круг закончился. Проверить, не достигла ли одна из команд победных очков (их очки >= victory_score).
Если достигла, вывести def congratulate. Если не достигла, вызвать старт следующего круга (def start_circle)

        :param event:
        :return:
        """
        user_id = event.user_id
        keyboard = VkKeyboard()
        self.bot.send_empty_keyboard(event,
                                     'Были объяснены слова:')
        self.bot.send_empty_keyboard(event, '\n'.join(self.temp_words_list))
        self.bot.send_empty_keyboard(event,
                           'Сколько слов объяснено неправильно? Напишите цифру. Если все правильно, введите "0"')



    def finish_explanation_2(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        self.temporary_score_counter -= int(event.text)
        self.finish_explanation_3(event)

    def finish_explanation_3(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        print(self.bot.commands_score)
        if self.temporary_score_counter < 0:
            self.temporary_score_counter = 0

        self.bot.commands_score[self.active_command] += self.temporary_score_counter
        self.bot.send_empty_keyboard(event,
                                     f'Ваша команда набрала {self.temporary_score_counter} очков')
        self.finish_explanation_4(event)
    def finish_explanation_4(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Начать объяснение!', color=VkKeyboardColor.POSITIVE)
        if self.commands_counter + 1 < self.bot.users.get(user_id)['command_amount']:
            self.commands_counter += 1
            self.active_command = self.bot.users[user_id]['command_name'][self.commands_counter]
            self.bot._send_msg(user_id,
                               f"Объясняет команда {self.active_command}", keyboard)

        else:
            self.finish_circle(event)

    def finish_circle(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        for i in self.bot.commands_score:
            self.bot.send_empty_keyboard(event,
                           f'Команда {i} набрала {self.bot.commands_score[i]} очков')
        for i in self.bot.users[user_id]['command_name']:
            if self.bot.commands_score[i] >= self.bot.users[user_id]['score']:
                self.congratulate(event)
                break
        else:
            self.commands_counter = 0
            self.start_circle(event)



    def congratulate(self, event):
        user_id = event.user_id
        keyboard = VkKeyboard()
        keyboard.add_button(label='Сыграть ещё раз', color=VkKeyboardColor.POSITIVE)
        self.bot.send_empty_keyboard(event,
                                     'Игра окончена!')
        for i in self.bot.commands_score:
            if self.bot.commands_score[i] == max(self.bot.commands_score.values()):
                self.bot._send_msg(user_id,
                                     f'Победила команда {i}', keyboard)


    def zero_counter(self, event):
        user_id = event.user_id
        if not self.bot.users[user_id].get('words counter'):
            self.bot.users[user_id]['words counter'] = 0
        return self.bot.users[user_id]['words counter']

    def count_words(self, event):
        user_id = event.user_id
        self.words_counter += 1
        return self.words_counter

    def score_counter(self, command_title):
        self.bot.commands_score[command_title] += 1

    def commands_count(self, event):
        user_id = event.user_id
        self.commands_counter += 1
        if self.commands_counter >= self.bot.users.get(user_id)['command_amount']:
            self.commands_counter = 0

    def set_temp_counter_2zero(self):
        self.__temp_counter = 0

    def temp_score_counter(self):
        self.__temp_counter += 1

    # def finish_explaination(self, event):
    #     user_id = event.user_id
    #     self.bot._send_msg(user_id, "Время истекло!")
    #     print(self.bot.commands_score)
    #     self.commands_count(event)
    #     self.game_starter(event)


class Time:

    def __init__(self, bot):
        self.bot = bot
    def time_start(self):
        self.__time_start = time.perf_counter()

    def time_check(self, event):
        user_id = event.user_id
        self.time_current = time.perf_counter()
        if self.time_current - self.__time_start < self.bot.users[user_id]['explain_time']:
            return True
        else:
            return False
class Counters:pass
    pass

class Images:
    def __init__(self, bot):
        self.bot = bot
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
