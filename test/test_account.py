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
    def tearDownClass(cls):
        cls.remove_account_file()

    @classmethod
    def setUpClass(cls):
        this_file_path = os.path.abspath(__file__)
        current_directory_path = os.path.dirname(this_file_path)
        target_yaml_file = 'test.yaml'
        cls.account_file_path = os.path.join(current_directory_path, target_yaml_file)
        cls.remove_account_file()
        # class to be tested
        cls.account_editor = AccountEditor(cls.account_file_path)

    @classmethod
    def remove_account_file(cls):
        try:
            with open(cls.account_file_path, 'r'):
                pass
            os.remove(cls.account_file_path)
        except IOError:
            pass


    def test_add_new_acount_when_not_exist_account_file(self):
        '''
        [test conditions] remove the account file
        [test success condition] A new account file with new account is created
        '''
        new_account_email = 'your@email.com'
        new_account_password = 'your_password'
        # test method
        self.account_editor.add_new_account(new_account_email, new_account_password)

        # check result
        try:
            with open(self.account_file_path, 'r') as file:
                account = yaml.load(file)

        except IOError:
            self.assertTrue(False)

        self.assertTrue(pbkdf2_sha256.verify(new_account_password, account[new_account_email][Item.PASSWORD.value]))
        
    def test_add_new_acount_when_exist_account_file(self):
        '''
        [test conditions] exist the account file
        [test success condition] A new account is in the account file
        '''
        pass

    def test_add_acount_failure_with_duplicate_account(self):
        pass

    def test_initalize_account_file(self):
        '''
        [test conditions] exist the account file
        [test success condition] A new account file with new account is created
        '''
        pass

    def test_login_success(self):
        pass

    def test_login_failure_with_wrong_email(self):
        pass

    def test_login_failure_with_wrong_password(self):
        pass

    def test_not_login_default_account(self):
        pass

    def test_update_account_email(self):
        pass

    def test_update_account_password(self):
        pass

    def test_delte_account(self):
        pass

    def test_delte_account_failure_with_delet_all_account(self):
        pass

if __name__ == '__main__':
    unittest.main()
