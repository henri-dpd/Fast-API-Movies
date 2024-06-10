from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        'year': 2009,
        'rating': 7.8,
        'category': 'action'
    },
    {
        'id': 2,
        'title': 'Shrek II',
        'overview': "Shrek y Fiona se casan, luego de la luna de miel son invitados a Muy Muy Lejano...",
        'year': 2005,
        'rating': 8.8,
        'category': 'fantasy'
    },
    {
        'id': 3,
        'title': 'Kung Fu Panda',
        'overview': "Un panda ha sido elegido como el guerrero dragón quien tiene la missión...",
        'year': 2005,
        'rating': 8.2,
        'category': 'action'
    }
]

app = FastAPI()
app.title = 'Fast API'
app.version = '0.0.1'

@app.get('/', tags=['home'])
def getHome():
    return HTMLResponse("<h1>Hello world!<h1>")

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    for movie in movies:
        if id == movie['id']:
            return movie
    return

@app.get("/movies/", tags=['movies'])
def get_movie_by_category(title: str = '', overview: str = '', category: str = '', year: int = -1, ratingDown: float = 0, ratingUp: float = 10):
    def filter(movie):
        return title in movie['title'] and overview in movie['overview'] and (category == '' or category == movie["category"]) and (year == -1 or year == movie['year']) and ratingDown>=movie['rating'] and ratingUp<=movie['rating']
    return [movie for movie in movies if filter(movie)]

@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), category: str = Body(), year: int = Body(), rating: float = Body()):
    if id < 0 or title == '' or category == "":
        return 'Invalid input'
    for movie in movies:
        if movie['id'] == id:
            return 'Movie already exist'
    movies.append({
        'id': id,
        "title": title,
        'overview': overview,
        'category': category,
        'year': year,
        'rating': rating
    })
    return movies

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, title: str = Body(), overview: str = Body(), category: str = Body(), year: int = Body(), rating: float = Body()):
    if id < 0:
        return f'invalid id: {id}'
    exist = False
    for movie in movies:
        if movie['id'] == id:
            movie.update({
                "id": id,
                "title": title,
                'overview': overview,
                'category': category,
                'year': year,
                'rating': rating
            })
            exist = True
    if not exist: return f'movie with id {id} do not exist'
    return movies

@app.delete('/movies/{id}', tags=['movies'])
def update_movie(id: int):
    if id < 0:
        return f'invalid id: {id}'
    exist = False
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            exist = True
    if not exist: return f'movie with id {id} do not exist'
    return movies
