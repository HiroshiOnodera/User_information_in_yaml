from passlib.hash import pbkdf2_sha256
from user_information_in_yaml.account.entry import Entry

class Password(Entry):

    def __init__(self, data : str):
        ''' overraide method
        '''
        self.__raw_password = data
        super().__init__(data)

    def __eq__(self, password : Entry) -> bool:
        ''' override method
        '''
        return pbkdf2_sha256.verify(self.__raw_password, password.value())

    def validate(self, data : str) -> bool:
        ''' override method
        '''
        if(not data or len(data) < 12 ):
            return False
        return True

    def exchange(self, data : str) -> str:
        ''' override method
        data exchange to hashed password
        '''
        return pbkdf2_sha256.hash(data)

    def verify(self, password : str) -> bool:
        return pbkdf2_sha256.verify(self.__raw_password, password)
