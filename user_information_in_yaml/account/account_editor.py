'''
account editor
'''
import yaml
from passlib.hash import pbkdf2_sha256
from user_information_in_yaml.account.item import Item

class AccountEditor():

    def __init__(self, account_file_path):
        self.account_file_path = account_file_path

    def add_new_account(self, email, password):
        ''' add new account that email and password
        Return none
        Raise IOError
        '''
        with open(self.account_file_path, 'w') as account_file:
            pass

        with open(self.account_file_path, 'r') as account_file:
            account = yaml.load(account_file)

        with open(self.account_file_path, 'w') as account_file:
            hash_password = pbkdf2_sha256.hash(password)
            account = {email : {Item.PASSWORD.value : hash_password}}
            yaml.dump(account, stream=account_file, default_flow_style=False)
