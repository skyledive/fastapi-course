from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field

### schema

### USERS

# user info
class User(BaseModel):
    email: EmailStr
    password: str

# user response
class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # Allow arbitrary types such as datetime
        from_attributes=True           # Ensure orm_mode compatibility
    )

### POSTS

# posts base: data expected to be received from the client (subset of table)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #optional response

# posts response: data sent back to client from api
class PostResponse(Post):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut # response model for user information beyond relational foreign key

    model_config = ConfigDict(
    arbitrary_types_allowed=True,  # Allow arbitrary types such as datetime
    from_attributes=True           # Ensure orm_mode compatibility
)
    
# posts response with join on votes
class PostVotesResponse(BaseModel):
    Post: PostResponse
    votes: int

    model_config = ConfigDict(
    arbitrary_types_allowed=True,  # Allow arbitrary types such as datetime
    from_attributes=True           # Ensure orm_mode compatibility
)

### AUTH

# user login
class UserLogin(User):
    pass

# user token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

### VOTE

# user vote
class UserVote(BaseModel):
    post_id: int
    direction: Annotated[int, Field(ge=0, le=1)]