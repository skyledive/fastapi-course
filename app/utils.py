from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
     # default password hashing algorithm
     return pwd_context.hash(password)

def verify(plain_password, hashed_password):
     # verify user password
     return pwd_context.verify(plain_password, hashed_password)