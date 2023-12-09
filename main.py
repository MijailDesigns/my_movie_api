from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
#Para cambiar el nombre de la aplicacion
app.title = "My app with FastAPI"
#Para cambiar la version de la aplicacion
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

#incluir los routes a la app
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

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




    

