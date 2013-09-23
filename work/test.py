#-*- coding: utf-8 -*-

calls = 0
def tracer(func):
	def wrapper(*args, **kwargs):
		global calls
		calls += 1
		print 'calls %s to %s' % (calls, func.__name__)
		return func(*args, **kwargs)
	return wrapper

@tracer
def spam(a, b, c):
	print a + b + c

spam(1, 2, 3)