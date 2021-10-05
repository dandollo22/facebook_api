import pydantic as _pydantic


class FacebookPost(_pydantic.BaseModel):
    id: str
    post_url: str
    page: str
    shared_at: str
    likes: str
    comments: str
    shares: str

    class Config:
        orm_mode = True
