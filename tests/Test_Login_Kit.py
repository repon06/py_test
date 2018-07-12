import unittest

from page.Login_Page import Login_Page
from utils.DriverFactory import DriverFactory

test_data_positive = [
    ("username1@name.ru", "pass1"),
    ("username2@name.ru", "pass2"),
    ("username3@name.ru", "pass3"),
    ("username4@name.ru", "pass4")
]

test_data_negative = [
    # пустой пароль
    ("username1@name.ru", ""),
    # пустой логин
    ("", "pass1"),
    # все пусто
    ("", ""),

    # поменять местави
    ("pass1", "username1@name.ru"),

    # js html
    ("<script>alert(123)</script>", "pass1"),
    ("username1@name.ru", "<script>alert(123)</script>"),
    ("<form action='http://www.ya.ru'><input type='submit'></form>", "pass1"),
    ("username1@name.ru", "<form action='http://www.ya.ru'><input type='submit'></form>"),

    # регистры
    ("USERNAME1@NAME.RU", "pass1"),
    ("username1@name.ru", "PASS1"),
    ("USERNAME1@NAME.RU", "PASS1"),

    # с пробелами
    (" username1@name.ru", "pass1"),
    ("username1@name.ru ", "pass1"),
    ("username1@name.ru", " 123"),
    ("username1@name.ru", "123 "),
    ("   ", "   "),
    ("username1@name.ru", "   "),
    ("   ", "pass1"),

    # верный логин, неверный пароль
    ("username1@name.ru", "123"),
    ("username1@name.ru", "pass"),
    ("username1@name.ru", "@!$#^%&*()"),

    # неверный логин, верный пароль
    ("username@name.ru", "pass1"),
    ("username1", "pass1"),

    # неверный логин/пароль
    ("username@name.ru", "123"),
    ("username1", "pass1"),
    ("username1",
     "12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"),
    ("username1", "123456")
]


def test_autorize_negative_func(login, password):
    def _test_func(self):
        "авторизация тестовыми негативными наборами тест пользователей"

        login_page = Login_Page(selenium_driver=self.driver)
        error = login_page.login(login, password)
        self.assertEqual('Wrong password, try again', error, 'Ожидалась ошибка авторизации')

    return _test_func


def test_autorize_positive_func(login, password):
    def _test_func(self):
        "авторизация тестовыми наборами пользователей"

        login_page = Login_Page(selenium_driver=self.driver)
        paymentPage = login_page.login(login, password)
        self.assertTrue(paymentPage.is_PaymentPage(), 'не Ожидалось ошибки авторизации')

    return _test_func


class TestAutorization(unittest.TestCase):

    def setUp(self):
        self.driver = DriverFactory().get_web_driver("chrome")

    def tearDown(self):
        self.driver.close()


for i, (user, passwd) in enumerate(test_data_negative):
    setattr(TestAutorization, 'test_negat("{0}" : "{1}")'.format(user, passwd),
            test_autorize_negative_func(user, passwd))
for i, (user, passwd) in enumerate(test_data_positive):
    setattr(TestAutorization, 'test_posit("{0}" : "{1}")'.format(user, passwd),
            test_autorize_positive_func(user, passwd))

if __name__ == "__main__":
    unittest.main()
