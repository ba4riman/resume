#-*- coding: utf-8 -*-
import time

def timer(func):
	def wrapper():
		t = time.time()
		res = func()
		print time.time() - t
		return res
	return wrapper