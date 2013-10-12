#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import datetime
import time
import cookielib
from decor import timer

@timer
def cinemas_in_kiev():

	def give_me_cookie():
		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie), urllib2.HTTPHandler())
		return opener

	# Открываем ссылку, если он доступна и считываем ее BeautifulSoup'ом
	page = urllib2.urlopen('http://www.okino.ua/kinoteatri-kieva/')
	if page.getcode() == 200:
		soup = BeautifulSoup(page.read(), from_encoding='utf-8')

		# Находим на странице все элементы ul с классом blist и открываем файл для записи
		ul = soup.findAll('ul', {'class': 'blist'})
		title = soup.find('h1', {'class': 'left'})

		# Находим все элементы списка с пустым id и формируем из полученного результата
		# xml-разметку, после чего сохраняем файл
		xml = ''
		for i in ul:
			for j in i.findAll('li', id=None):

				# Извлекаем id из ссылки на описание кинотеатра
				for a in j.findAll('a'):
					href = a['href']
					num = re.compile(r'\d+')
					take_num = num.search(href).group()
					id = int(take_num)

					name = j.string.replace(u'Кинотеатр', '').strip()
					xml += '<name id="%s">%s</name>\n' % (id, name) if len(name) >= 2 else '\n<category value="%s"></category>\n\n' % name[0]

					# Открываем, поочереди, описание кинотеатров, считываем адрес и записываем в xml
					opener = give_me_cookie()
					req = opener.open(urllib2.Request('http://www.okino.ua%s' % a.get('href'))) 
					if req.getcode() == 200:
						details = BeautifulSoup(req.read(), from_encoding='utf-8')
						for addr in details.findAll('span', itemprop='streetAddress'):
							xml += '<addres>%s</addres>\n' % addr.text

		open('cinemas.xml', 'w').write('<data value="%s">%s</data>' % (title.text.encode('utf-8'), xml.encode('utf-8')))


@timer
def schedules_in_kiev():

	# Записываем текущую дату в datenow и дату через 7 дней в datefuture.
	# Открываем файл для записи.
	datenow = datetime.datetime.now().date()
	datefuture = datenow + datetime.timedelta(days=7)
	xml = ''

	# Пока текущая дата не будет равна грядущей (datefuture), по очереди, открываем
	# все страницы с датами в этом диапазоне и парсим данные о сеансах в эти дни.
	while datenow != datefuture:
		xml += '<date value="%s">\n' % datenow.strftime('%Y-%m-%d')

		page = urllib2.urlopen('http://www.okino.ua/kinoafisha-kiev/?date=%s' % datenow.strftime('%Y-%m-%d'))
		datenow += datetime.timedelta(days=1)

		if page.getcode() == 200:
			soup = BeautifulSoup(page)
			films = soup.findAll('div', {'class': 'item0'})

			# Формируем xml разметку:
			for film in films:
				for head in zip(film.findAll('div', {'class': 'h3-wrap'}), film.findAll('a', href=re.compile('^/film'))): # названия кинотеатров
					a = head[1]
					href = a['href']
					id = re.compile(r'\d+')
					take_id = id.search(href).group()
					if len(take_id) == 6:
						int_id = int(take_id)
					cinema = head[0].text.encode('utf-8').strip()
					films = head[1].text.encode('utf-8').strip()

					xml += '<film>\n'
					xml += '<cinema>%s</cinema>\n' % (head[0].text.strip())

					for block in film.findAll('div', {'class': 'item2'}): 
						for name in block.findAll('div', {'class': 'name'}): # названия фильмов
							xml += '<name id="%s" value="%s">\n' % (int_id, name.text.strip())

							for times in block.findAll('div', {'class': 'showtime'}):
								for span in times.findAll('span'):          # время сенсов
									xml += '\t<time>%s</time>\n' % span.text.replace('\n', ' ')

							xml += '</name>\n'
					xml += '</film>\n'

		xml += '</date>'

	# Записываем и сохраняем данные в файл
	open('schedules.xml', 'w').write('<data>\n%s</data>' % xml.encode('utf-8'))


@timer
def films_in_kiev():

	# Записываем текущую дату в datenow и дату через 7 дней в datefuture.
	# Открываем файл для записи.
	datenow = datetime.datetime.now().date()
	datefuture = datenow + datetime.timedelta(days=7)
	xml = ''

	def give_me_cookie():
		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie), urllib2.HTTPHandler())
		return opener

	opener = give_me_cookie()

	# Пока текущая дата не будет равна грядущей (datefuture), по очереди, открываем
	# все страницы с датами в этом диапазоне и парсим данные о сеансах в эти дни.
	while datenow != datefuture:
		xml += '<date value="%s">\n' % datenow.strftime('%Y-%m-%d')

		page = urllib2.urlopen('http://www.okino.ua/kinoafisha-kiev/?date=%s' % datenow.strftime('%Y-%m-%d'))
		datenow += datetime.timedelta(days=1)
		if page.getcode() == 200:
			soup = BeautifulSoup(page.read(), from_encoding='utf-8')
			for films in soup.findAll('div', {'class': 'name'}):
				try:
					href = films.a['href']
					id = re.compile(r'\d+')
					take_id = id.search(href).group()
					if len(take_id) == 6:
						int_id = int(take_id)
				except TypeError:
					pass
				try:
					xml += '<film value="%s">\n' % films.a.string
				except AttributeError:
					xml += '<film value="%s">\n' % films.string.strip()

	open('films.xml', 'w').write('<data>\n%s</data>' % xml.encode('utf-8'))


if __name__ == '__main__':
	#cinemas_in_kiev()
	#schedules_in_kiev()
	films_in_kiev()