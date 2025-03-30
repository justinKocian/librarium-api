from pydantic import BaseModel

class SeriesBase(BaseModel):
    name: str

class SeriesCreate(SeriesBase):
    pass

class SeriesRead(SeriesBase):
    id: int

    model_config = {
        "from_attributes": True
    }