'''
account contrller
'''
import yaml
from passlib.hash import pbkdf2_sha256
from user_information_in_yaml.account.item import Item
from user_information_in_yaml.account.email import Email


class Account():

    def __init__(self, account_file_path):
        self.account_file_path = account_file_path

    def __write_accoutn_file(self, account: dict) -> None:
        with open(self.account_file_path, 'w') as account_file:
            yaml.dump(account, stream=account_file, default_flow_style=False)

    def __load_account_file(self) -> dict:
        with open(self.account_file_path, 'r') as account_file:
            return yaml.load(account_file)

    def add(self, email: Email, password: str) -> None:
        ''' add new account that email and password
        Raise KeyError
        '''
        if(not password): raise TypeError

        hash_password = pbkdf2_sha256.hash(password)

        try:
            account = self.__load_account_file()
            if(email.value() in account):
                raise KeyError
            account[email.value()] = {Item.PASSWORD.value: hash_password}
        except IOError:
            with open(self.account_file_path, 'w'):
                account = {email.value(): {Item.PASSWORD.value: hash_password}}

        self.__write_accoutn_file(account)

    def authenticate(self, email: Email, password: str) -> bool:
        ''' authenticate using email and password
        '''
        try:
            account = self.__load_account_file()
        except IOError:
            return False

        try:
            return pbkdf2_sha256.verify(password, account[email.value()][Item.PASSWORD.value])
        except KeyError:
            return False

    def delete(self, email: Email) -> None:
        ''' delete account using email
        Raises KeyError when The account file not have the email
        Raises RuntimeError when The account file have one account
        '''
        account = self.__load_account_file()
        account.pop(email.value())
        if(not account):
            raise RuntimeError

        self.__write_accoutn_file(account)

    def initalize(self, default_account_email : Email, default_account_password : str) -> None:
        ''' initalize account file
        all account delete and create default account
        '''
        if(not default_account_password): raise TypeError
        account = self.__load_account_file()
        account.clear()
        hash_password = pbkdf2_sha256.hash(default_account_password)
        account[default_account_email.value()] = {Item.PASSWORD.value : hash_password}
        self.__write_accoutn_file(account)

    def update_password(self, email : Email, password : str) -> None:
        ''' update account password
        Raises KeyError
        '''
        if(not password): raise TypeError
        account = self.__load_account_file()
        hash_password = pbkdf2_sha256.hash(password)
        account[email.value()][Item.PASSWORD.value] = hash_password
        self.__write_accoutn_file(account)
