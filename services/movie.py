from models.movie import Movie as MovieModel
from schemas.movie import Movie


class MovieService():

    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movies_by_category(self, category):
        result = self.db.query(MovieModel).filter_by(category = category).all()
        return result
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    def update_movie(self, id, data: Movie):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id)
        movie.update(dict(data), synchronize_session=False)
        self.db.commit()

    def delete_movie(self, id):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(movie)
        self.db.commit()