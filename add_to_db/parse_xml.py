#-*- coding: utf-8 -*-

import MySQLdb

from bs4 import BeautifulStoneSoup

db = MySQLdb.connect('localhost', 'root', '80671551192', 'test')
cursor = db.cursor()
xml_cinema = open('dumps/cinema.xml')
soup = BeautifulStoneSoup(xml_cinema)

for i in soup.findAll('cinema'):
	id = int(i['id'])
	cinema = i['name'].encode('utf-8')
	city_id = int(i['id'])
	cinema_circuit_id = ''
	street_type_id = ''
	street_name = ''
	number_housing = ''
	number_hous = ''
	letter_housing = ''
	try:
		zip = int(i.zip['value'])
	except ValueError:
		zip = 0
	opening = ''
	note = ''
	code = ''

	coding = "SET NAMES 'utf8'"
	cursor.execute(coding)
	sql = "INSERT INTO cinema (id, name, zip) VALUES ('%s', '%s', '%s')" % (id, cinema, zip)
	cursor.execute(sql)

db.commit()
db.close()