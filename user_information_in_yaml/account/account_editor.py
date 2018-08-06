'''
account contrller
'''
import yaml
from passlib.hash import pbkdf2_sha256
from user_information_in_yaml.account.item import Item


class Account():

    def __init__(self, account_file_path):
        self.account_file_path = account_file_path

    def __write_accoutn_file(self, account: dict) -> None:
        with open(self.account_file_path, 'w') as account_file:
            yaml.dump(account, stream=account_file, default_flow_style=False)

    def __load_account_file(self) -> dict:
        with open(self.account_file_path, 'r') as account_file:
            return yaml.load(account_file)

    def add(self, email: str, password: str) -> None:
        ''' add new account that email and password
        Raise KeyError
        '''
        hash_password = pbkdf2_sha256.hash(password)

        try:
            account = self.__load_account_file()
            if(email in account):
                raise KeyError
            account[email] = {Item.PASSWORD.value: hash_password}
        except IOError:
            with open(self.account_file_path, 'w'):
                account = {email: {Item.PASSWORD.value: hash_password}}

        self.__write_accoutn_file(account)

    def authenticate(self, email: str, password: str) -> bool:
        ''' authenticate using email and password
        '''
        try:
            account = self.__load_account_file()
        except IOError:
            return False

        try:
            return pbkdf2_sha256.verify(password, account[email][Item.PASSWORD.value])
        except KeyError:
            return False

    def delete(self, email: str) -> None:
        ''' delete account using email
        Raises KeyError when The account file not have the email
        Raises RuntimeError when The account file have one account
        '''
        account = self.__load_account_file()
        account.pop(email)
        if(not account):
            raise RuntimeError

        self.__write_accoutn_file(account)
