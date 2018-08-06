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
from user_information_in_yaml.account.account_editor import AccountEditor
from user_information_in_yaml.account.item import Item


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
        cls.account = AccountEditor(cls.account_file_path)
        pass

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
        new_account_email_1 = 'your1@email.com'
        new_account_password_1 = 'your1_password'
        new_account_email_2 = 'your2@email.com'
        new_account_password_2 = 'your2_password'
        error_account_email = 'error@email.com'
        error_account_password = 'error_password'

        self.account.add_account(new_account_email_1, new_account_password_1)
        self.account.add_account(new_account_email_2, new_account_password_2)

        self.assertTrue(self.account.authenticate(
            new_account_email_1, new_account_password_1))
        self.assertTrue(self.account.authenticate(
            new_account_email_2, new_account_password_2))
        self.assertFalse(self.account.authenticate(
            new_account_email_1, error_account_password))
        self.assertFalse(self.account.authenticate(
            error_account_email, error_account_password))

    def test_add_acount_failure_with_duplicate_account(self):
        '''
        [test conditions] add two same email account
        [test success condition] raise KeyError
        '''
        new_account_email_1 = 'your1@email.com'
        new_account_password_1 = 'your1_password'
        self.account.add_account(new_account_email_1, new_account_password_1)

        with self.assertRaises(KeyError):
            self.account.add_account(
                new_account_email_1, new_account_password_1)

    def test_authenticate_with_no_account_file(self):
        email = 'your@email.com'
        password = 'your_password'

        self.assertFalse(self.account.authenticate(email, password))

    def test_initalize_account_file(self):
        '''
        [test conditions] exist the account file
        [test success condition] A new account file with new account is created
        '''
        pass

    def test_update_account_email(self):
        pass

    def test_update_account_password(self):
        pass

    def test_delte_account(self):
        '''
        [test conditions] There are accounts in the account file
        [test success condition] The account is deleted
        '''
        account_email_deleted = 'your1@email.com'
        account_password_deleted = 'your1_password'
        account_email = 'your2@email.com'
        account_password = 'your2_password'
        account_email_error = 'error@email.com'
        account_password_error = 'error_password'

        self.account.add_account(
            account_email_deleted, account_password_deleted)
        self.account.add_account(account_email, account_password)
        self.account.delete_account(account_email_deleted)

        self.assertTrue(self.account.authenticate(
            account_email, account_password))
        self.assertFalse(self.account.authenticate(
            account_email_deleted, account_password_deleted))

        with self.assertRaises(KeyError):
            self.account.delete_account(account_email_error)

        self.assertFalse(self.account.authenticate(
            account_email_error, account_password_error))

    def test_delte_account_failure_with_delet_all_account(self):
        '''
        [test conditions] There an accounts in the account file
        [test success condition] The last account is left in the account file
        '''
        account_email_deleted = 'your1@email.com'
        account_password_deleted = 'your1_password'
        self.account.add_account(
            account_email_deleted, account_password_deleted)

        with self.assertRaises(RuntimeError):
            self.account.delete_account(account_email_deleted)

        self.assertTrue(self.account.authenticate(account_email_deleted, account_password_deleted))


if __name__ == '__main__':
    unittest.main()
