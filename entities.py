'''Entity classes for better management of Redis Online Conference Tool.'''

class User:
    '''
    A class to represent a user in the online conference tool.

    Attributes
    ----------
    id : str
        a unique identifier
    name : str
        the name of the user
    age : int
        how old the user is
    gender : str
        Male or Female, how the user identifies
    email : str
        the email address the user uses
    '''

    def __init__(self, user: dict):
        '''
        Parameters
        ----------
        user : dict
            a dictionary that contains the attributes of the user
        '''
        self.id = user['userID']
        self.name = user['name']
        self.age = user['age']
        self.gender = user['gender']
        self.email = user['email']

    def __str__(self) -> str:
        return f'User(\n\
            id: {self.id},\n\
            name: {self.name},\n\
            age: {self.age},\n\
            gender: {self.gender},\n\
            email: {self.email})'


class Meeting:
    '''
    A class to represent a meeting in the online conference tool.

    Attributes
    ----------
    id : str
        a unique identifier
    title : str
        the title of the meeting
    description : str
        the description of the meeting
    is_public : int
        1 if the meeting is public, 0 otherwise
    audience : list
        a list containing all the email addresses of participants if
        the meeting isn't public
    '''

    def __init__(self, meeting: dict):
        '''
        Parameters
        ----------
        user : dict
            a dictionary that contains the attributes of the meeting
        '''
        self.id = meeting['meeting_id']
        self.title = meeting['title']
        self.description = meeting['description']
        self.is_public = meeting['isPublic']
        self.audience = meeting['audience']

    def __str__(self) -> str:
        return f'Meeting(\n\
            id: {self.id},\n\
            title: {self.title},\n\
            description{self.description},\n\
            is_public: {self.is_public},\n\
            audience: {self.audience})'