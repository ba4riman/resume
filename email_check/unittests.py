#-*- coding: utf-8 -*-
import unittest
from email_check import email_check

class TestCorrectEmail(unittest.TestCase):

    def setUp(self):
        self.mails = ['a@m.m', '01mail_na-me@mail.com.com', '01mailna-me@mail.com', '01mail""na-me@mail.com', '01mail"!,:"na-me@mail.com', '01mail.na-me@mail.com']

    def test_email_check(self):
        for i in self.mails:
            self.assertTrue(i == email_check(i), 'Некорректное значение')

    def tearDown(self):
        self.mails = None

if __name__ == '__main__':
    unittest.main()