from fastapi import Depends, FastAPI, HTTPException, Body, Query, Path, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie

app = FastAPI()
#Para cambiar el nombre de la aplicacion
app.title = "My app with FastAPI"
#Para cambiar la version de la aplicacion
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
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

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
     {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Drama'    
    } 
]

#los tags nos permite agrupar las rutas de la aplicacion
@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=404, content={"message": "Credenciales inválidas, intente de nuevo"})

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    try:
        movie = list(filter(lambda movie: movie['id'] == id, movies))[0]
        return JSONResponse(status_code=200, content=movie)
    except IndexError as error:
        print(error)
        raise HTTPException(status_code=404, detail=f"Movie with id {id} not found")
    
@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category:str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [item for item in movies if item['category'] == category]
    return JSONResponse(status_code=200, content=data)

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la pelicula"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id:int, movie: Movie = Body()) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula"})
    raise HTTPException(status_code=404, detail=f"Movie with id {id} not found")

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id:int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula"})
    raise HTTPException(status_code=404, detail=f"Movie with id {id} not found")
    

