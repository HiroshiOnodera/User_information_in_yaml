'''
account editor
'''
import yaml
from passlib.hash import pbkdf2_sha256
from user_information_in_yaml.account.item import Item

class AccountEditor():

    def __init__(self, account_file_path):
        self.account_file_path = account_file_path

    def add_account(self, email : str, password : str) -> None:
        ''' add new account that email and password
        Raise IOError
        '''
        hash_password = pbkdf2_sha256.hash(password)

        try:
            with open(self.account_file_path, 'r') as account_file:
                account = yaml.load(account_file)
                account[email] = {Item.PASSWORD.value : hash_password}

        except IOError:
            with open(self.account_file_path, 'w') as account_file:
                account = {email : {Item.PASSWORD.value : hash_password}}

        with open(self.account_file_path, 'w') as account_file:
            yaml.dump(account, stream=account_file, default_flow_style=False)

    def authenticate(self, email : str, password : str) -> bool:
        ''' authenticate using email and password
        '''
        try:
            with open(self.account_file_path, 'r') as account_file:
                account = yaml.load(account_file)
        except IOError:
            return False

        try:
            return pbkdf2_sha256.verify(password, account[email][Item.PASSWORD.value])

        except KeyError:
            return False
