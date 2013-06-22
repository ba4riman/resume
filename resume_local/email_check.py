#-*- coding: utf-8 -*-
import re

def email_check(mail):
	"""
	Доменная и именная части разделены символом "@".
	Доменная часть является набором строк разделенных точкой.

	Размер именной части не меньше 1 символа.
	Размер доменной - не меньше 3 символов
	>>> email_check('a@m.m')
	'a@m.m'
	>>> email_check('01mail_na-me@mail.com.com')
	'01mail_na-me@mail.com.com'

	В именной части могут содержаться цифры, буквы и символы
	>>> email_check('01mailna-me@mail.com')
	'01mailna-me@mail.com'

	Кавычки могут быть только парными
	>>> email_check('01mail""na-me@mail.com')
	'01mail""na-me@mail.com'

	Символы "!,:" в именной части могут быть толкьо в кавычках
	>>> email_check('01mail"!,:"na-me@mail.com')
	'01mail"!,:"na-me@mail.com'

	В именной части точки не могут идти друг за другом
	>>> email_check('01mail.na-me@mail.com')
	'01mail.na-me@mail.com'
	"""
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
	result = compil.search(mail)
	if result:
		length = mail.split('@')
		if len(length[0]) <= 128 and len(length[1]) <= 256:
			return mail if not '-.' in length[1] and not '.-' in length[1] else 'Dash error'
		else:
			print 'E-mail length is not correct'
	else:
		print 'E-mail is not correct'

if __name__ == '__main__':
	import doctest
	doctest.testmod(verbose=True)