from passlib.hash import pbkdf2_sha256
from user_information_in_yaml.account.entry import Entry

class Password(Entry):

    def __eq__(self, password : Entry) -> bool:
        ''' override method
        '''
        return pbkdf2_sha256.verify(super().value(), password.value())

    def validate(self, data : str) -> bool:
        ''' override method
        '''
        if(not data or len(data) < 12 ):
            return False
        return True

    def value(self) -> str:
        ''' override method
        data change to hashed password
        '''
        return pbkdf2_sha256.hash(super().value())

    def verify(self, hash_password : str) -> bool:
        return pbkdf2_sha256.verify(super().value(), hash_password)
