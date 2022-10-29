import random


print('Привет, давай поиграем. Я загадал число от 1 до 100. Называй свой вариант, а я буду говорить: большие или меньше')
x = random.randint(1, 100)


def poll():
    y = int(input('Твой вариант? '))
    try:
        if y == x:
            print('Ты угадал.')

        elif 101 > y > x:
            print('Меньше.')
            poll()
        elif 1 < y < x:
            print('Больше')
            poll()
        elif y > 100 or y < 1:
            print('Число должно быть от 1 до 100.')
            poll()
    except TypeError:
        print('Ты ввёл не число.')

poll()