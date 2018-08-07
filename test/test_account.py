'''
test account edit function

* initialize the account yaml file and write only the default account to the account yaml file.
* update email and password of the account yaml file.
* add new account to the account yaml file.
* delete account to the account yaml file.
'''
import unittest
import os
import yaml
from passlib.hash import pbkdf2_sha256
from user_information_in_yaml.account.account import Account
from user_information_in_yaml.account.item import Item
from user_information_in_yaml.account.email import Email
from user_information_in_yaml.account.password import Password


class TestAccountPakage(unittest.TestCase):
    ''' test case
    target file is account_editor.py
    '''

    @classmethod
    def setUpClass(cls):
        this_file_path = os.path.abspath(__file__)
        current_directory_path = os.path.dirname(this_file_path)
        target_yaml_file = 'test.yaml'
        cls.account_file_path = os.path.join(
            current_directory_path, target_yaml_file)
        cls.remove_account_file()

    @classmethod
    def setUp(cls):
        # class to be tested
        cls.account = Account(cls.account_file_path)

    @classmethod
    def tearDown(cls):
        cls.remove_account_file()

    @classmethod
    def remove_account_file(cls):
        try:
            with open(cls.account_file_path, 'r'):
                pass
            os.remove(cls.account_file_path)
        except IOError:
            pass

    def test_add_acount(self):
        '''
        [test conditions] remove the account file
        [test success condition] A new account file with new account is created and authenticate new account
        '''
        new_account_email_1 = Email('your1@email.com')
        new_account_password_1 = Password('your1_password')
        new_account_email_2 = Email('your2@email.com')
        new_account_password_2 = Password('your2_password')

        self.account.add(new_account_email_1, new_account_password_1)
        self.account.add(new_account_email_2, new_account_password_2)

        self.assertTrue(self.account.authenticate(
            new_account_email_1, new_account_password_1))
        self.assertTrue(self.account.authenticate(
            new_account_email_2, new_account_password_2))

        error_account_email = Email('error@email.com')
        error_account_password = Password('error_password')
        self.assertFalse(self.account.authenticate(
            new_account_email_1, error_account_password))
        self.assertFalse(self.account.authenticate(
            error_account_email, error_account_password))


    def test_add_acount_failure_with_duplicate_account(self):
        '''
        [test conditions] add two same email account
        [test success condition] raise KeyError
        '''
        new_account_email_1 = Email('your1@email.com')
        new_account_password_1 = Password('your1_password')
        self.account.add(new_account_email_1, new_account_password_1)

        with self.assertRaises(KeyError):
            self.account.add(new_account_email_1, new_account_password_1)

    def test_authenticate_with_no_account_file(self):
        email = Email('your@email.com')
        password = Password('your_password')

        self.assertFalse(self.account.authenticate(email, password))

    def test_initalize_account_file(self):
        '''
        [test conditions] exist the account file
        [test success condition] A new account file with new account is created
        '''
        account_email = Email('your@mail.com')
        account_password = Password('your_password')
        self.account.add(account_email, account_password)

        new_account_email = Email('new_your@mail.com')
        new_account_password = Password('new_your_password')
        self.account.initalize(new_account_email, new_account_password)

        self.assertFalse(self.account.authenticate(account_email, account_password))
        self.assertTrue(self.account.authenticate(new_account_email, new_account_password))

    def test_update_account_email(self):
        '''
        [test conditions] exist the account file
        [test success condition] The account's email is changed
        '''
        account_email = Email('your@email.com')
        account_password = Password('your_password')
        self.account.add(account_email, account_password)

        changed_account_email = Email('changed@email.com')
        self.account.update_email(account_email, changed_account_email)
        self.assertTrue(self.account.authenticate(
            changed_account_email, account_password))
        self.assertFalse(self.account.authenticate(
            account_email, account_password))

        error_account_email = Email('error@mail.com')
        error_account_new_email = Email('error_new@mail.com')
        with self.assertRaises(KeyError):
            self.account.update_email(
                error_account_email, error_account_new_email)

    def test_update_account_password(self):
        '''
        [test conditions] exist the account file
        [test success condition] The account's password is changed
        '''
        account_email = Email('your@email.com')
        account_password = Password('your_password')
        self.account.add(account_email, account_password)

        changed_account_password = Password('changed_password')
        self.account.update_password(account_email, changed_account_password)
        self.assertTrue(self.account.authenticate(
            account_email, changed_account_password))
        self.assertFalse(self.account.authenticate(
            account_email, account_password))

        error_account_email = Email('error@mail.com')
        error_account_password = Password('error_password')
        with self.assertRaises(KeyError):
            self.account.update_password(
                error_account_email, error_account_password)


    def test_delte_account(self):
        '''
        [test conditions] There are accounts in the account file
        [test success condition] The account is deleted
        '''
        account_email_deleted = Email('your1@email.com')
        account_password_deleted = Password('your1_password')
        account_email = Email('your2@email.com')
        account_password = Password('your2_password')

        self.account.add(account_email_deleted, account_password_deleted)
        self.account.add(account_email, account_password)
        self.account.delete(account_email_deleted)

        self.assertTrue(self.account.authenticate(
            account_email, account_password))
        self.assertFalse(self.account.authenticate(
            account_email_deleted, account_password_deleted))

        account_email_error = Email('error@email.com')
        account_password_error = Password('error_password')

        with self.assertRaises(KeyError):
            self.account.delete(account_email_error)

        self.assertFalse(self.account.authenticate(
            account_email_error, account_password_error))

    def test_delte_account_failure_with_delet_all_account(self):
        '''
        [test conditions] There an accounts in the account file
        [test success condition] The last account is left in the account file
        '''
        account_email_deleted = Email('your1@email.com')
        account_password_deleted = Password('your1_password')
        self.account.add(
            account_email_deleted, account_password_deleted)

        with self.assertRaises(RuntimeError):
            self.account.delete(account_email_deleted)

        self.assertTrue(self.account.authenticate(
            account_email_deleted, account_password_deleted))

    def test_email_value(self):
        value = 'your@email.com'
        self.assertEqual(Email(value), Email(value))

        with self.assertRaises(TypeError):
            Email(None)
        with self.assertRaises(TypeError):
            Email('')
        with self.assertRaises(TypeError):
            Email('email')  # '@' is not in email string

    def test_password_value(self):
        value = 'password0123'

        self.assertTrue(pbkdf2_sha256.verify(value, Password(value).value()))
        self.assertEqual(Password(value), Password(value))

        with self.assertRaises(TypeError):
            Password(None)
        with self.assertRaises(TypeError):
            Password('')
        with self.assertRaises(TypeError):
            Password('12345678901')


if __name__ == '__main__':
    unittest.main()
