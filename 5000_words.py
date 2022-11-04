FILE = r'C:\Users\USER\PycharmProjects\Bot\5000_words.txt'
FILE2 = r'C:\Users\USER\PycharmProjects\Bot\file.txt'

with open (FILE, encoding="utf8") as f:
    line = f.read()
    while line:
        for i in line:
            if i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'x', 'y', 'z']:
                with open (FILE2, 'a') as file:
                    file.write(i)
            elif i == ';':
                with open(FILE2, 'a') as file:
                    file.write("\n")
        break

with open (FILE2) as f:
    list = f.readlines()
    list = [line.rstrip('\n') for line in list]

print(list)
print('Я закончил')

['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
#            'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']:




