#-*- coding: utf-8 -*-
import re

def email_check(mail): # В качестве аргумента передается email.
	# Регулярное выражение компилируется в объект шаблона.
	compil = re.compile(r"""
		^([-a-z0-9_]+
			((?![.][.])|([.]))
			((["]["])|(["][!:,]+["]))?
		([-a-z0-9_]+)?)
		@
		[-a-z0-9_]+
		[.]
		([-a-z0-9_]+
			([.][-a-z0-9_]+)?
		)$
		""", re.X)

	# Сканирование email(передаваемого ф-ии в качестве аргумента)
	# на совпадения с регулярным выражением.
	result = compil.search(mail)

	# Проверка на максимальную и минимальную длинну именной, а также
	# ограничение на наличие символа "-" в словах между точками.
	if result:
		length = mail.split('@')
		if len(length[0]) <= 128 and len(length[1]) <= 256:
			print mail, 'подходит' if not '-.' in length[1] and not '.-' in length[1] else 'Недопустимое значени'
		else:
			print 'Длинна строки не соответствует'
	else:
		print 'Некорректный ввод данных'
	return result.group()

# Исполнение doc-тестов из файла test.txt при условии,
# что файл email_check.py является вызываемым, а не импортируемым
#if __name__ == '__main__':
	#import doctest
	#doctest.testfile('test.txt', verbose=True)
	#unittest.main()