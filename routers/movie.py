from fastapi import APIRouter, Depends, Body, Query, Path, Request
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    # result = db.query(MovieModel).all()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    # try:
    #     movie = list(filter(lambda movie: movie['id'] == id, movies))[0]
    #     return JSONResponse(status_code=200, content=movie)
    # except IndexError as error:
    #     print(error)
    #     raise HTTPException(status_code=404, detail=f"Movie with id {id} not found")
    
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category:str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    # result = db.query(MovieModel).filter_by(category = category).all()
    # print(result)
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    # data = [item for item in movies if item['category'] == category]
    # return JSONResponse(status_code=200, content=data)

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    #creo una sesion de db
    db = Session()
    # creo una instancia de movie
    # new_movie = MovieModel(**movie.model_dump())
    # lo inserto
    #db.add(new_movie)
    # actualizo para que se guarden los cambios
    # db.commit()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la pelicula"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id:int, movie: Movie = Body()) -> dict:
    # db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id).first()
    # if not result:
    #     return JSONResponse(status_code=404, content={'message': "No encontrado"})
    # result.title = movie.title
    # result.category = movie.category
    # result.overview = movie.overview
    # result.rating = movie.rating
    # result.year = movie.year
    # db.commit()
    # return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula"})

    #Another solution
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id)
    # if not result.scalar():
    #     return JSONResponse(status_code=404, content={'message': "No encontrado"})
    # result.update(dict(movie), synchronize_session=False)
    # db.commit()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula"})
    # for item in movies:
    #     if item['id'] == id:
    #         item['title'] = movie.title
    #         item['overview'] = movie.overview
    #         item['year'] = movie.year
    #         item['rating'] = movie.rating
    #         item['category'] = movie.category
    #         return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula"})
    # raise HTTPException(status_code=404, detail=f"Movie with id {id} not found")

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id:int) -> dict:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id).first()
    # if not result:
    #     return JSONResponse(status_code=404, content={'message': "No encontrado"})
    # db.delete(result)
    # db.commit()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula"})
    # for item in movies:
    #     if item['id'] == id:
    #         movies.remove(item)
    #         return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula"})
    # raise HTTPException(status_code=404, detail=f"Movie with id {id} not found")