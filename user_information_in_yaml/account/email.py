from user_information_in_yaml.account.entry import Entry

class Email(Entry):

    def __eq__(self, email : Entry) -> bool:
        ''' override method
        '''
        return super().value() == email.value()

    def validate(self, data : str) -> bool:
        ''' override method
        '''
        if(not data or len(data) < 1 or '@' not in data):
            return False
        return True
