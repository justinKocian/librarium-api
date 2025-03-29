from pydantic import BaseModel

class SeriesBase(BaseModel):
    name: str

class SeriesCreate(SeriesBase):
    pass

class SeriesRead(SeriesBase):
    id: int

    class Config:
        from_attributes = True
