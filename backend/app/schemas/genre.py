from pydantic import BaseModel

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreBase):
    id: int

    model_config = {
        "from_attributes": True
    }
