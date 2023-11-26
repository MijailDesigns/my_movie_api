from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
#Para cambiar el nombre de la aplicacion
app.title = "My app with FastAPI"
#Para cambiar la version de la aplicacion
app.version = "0.0.1"

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

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}')
def get_movie(id: int):
    try:
        return list(filter(lambda movie: movie['id'] == id, movies))[0]
    except IndexError as error:
        print(error)
        raise HTTPException(status_code=404, detail=f"Movie with id {id} not found")
    
@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category:str, year: int):
    return [item for item in movies if item['category'] == category]
    # return category, year

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id:int, movie: Movie = Body()):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies
    raise HTTPException(status_code=404, detail=f"Movie with id {id} not found")

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id:int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies
    raise HTTPException(status_code=404, detail=f"Movie with id {id} not found")
    

