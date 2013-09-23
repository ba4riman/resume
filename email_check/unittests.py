import unittest

class Test(unittest.TestCase):
	def test_email_check(self):
		from email_check import email_check
		
		self.assertEqual(email_check('a@m.m'), 'a@m.m')
		self.assertEqual(email_check('01mail_na-me@mail.com.com'), '01mail_na-me@mail.com.com')

if __name__ == '__main__':
	unittest.main()