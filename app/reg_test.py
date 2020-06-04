import re

str = '''<a href="https://kino-teatr.ua/ru/main/films/year/2019.phtml" title="Фильмы 2019">2019</a><br/>
Страна: 
<a href="https://kino-teatr.ua/ru/main/films/country/17.phtml" title="Фильмы Южная Корея">Убить била</a><br/>'''

result = re.search(r'[>]\d+[<]', str)
print(result[0])
result = re.findall(r'>[а-яА-Я| ]+<', str)
print(result[0])

genre1 = 'Ужастик'
genre2 = 'Драма'

dic = {}

dic.setdefault('genre', genre1)
print(dic)
dic.update({'genre': dic['genre'] + f' {genre2}'})
print(dic)
