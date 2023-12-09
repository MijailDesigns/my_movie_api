from pydantic import BaseModel, Field

class Movie(BaseModel):
    # id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(ge=1, le=2023)
    rating: float = Field(ge= 0.1, le=10.0)
    category: str = Field(min_length=3, max_length=15)

    #Esto es para los campos por default
    class Config:
        #esto cambio en la V2 de fastapi, antes se colocaba solo schema_extra
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2023,
                "rating": 9.8,
                "category": "Acción"
            }
        }