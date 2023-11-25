from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.responses import HTMLResponse

app = FastAPI()
#Para cambiar el nombre de la aplicacion
app.title = "My app with FastAPI"
#Para cambiar la version de la aplicacion
app.version = "0.0.1"

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
def create_movie(id:int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return movies

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id:int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    for item in movies:
        if item['id'] == id:
            item['title'] = title
            item['overview'] = overview
            item['year'] = year
            item['rating'] = rating
            item['category'] = category
            return movies
    raise HTTPException(status_code=404, detail=f"Movie with id {id} not found")

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id:int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies
    raise HTTPException(status_code=404, detail=f"Movie with id {id} not found")
    

