
from typing import Optional
from ...domain.domainTypes import User

def parseUser(data: dict) -> Optional[User]:
    try:
        if not (type(data['name']) is str):
            return None
        if not (type(data['password']) is str):
            return None
        
        return User(data['name'], data['password'])
    except:
        return None
