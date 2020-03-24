from app_config import API_KEY, API_HOST
import requests
import json
from html import unescape
from models import db, SavedMovie

#TODO FIX THIS FOR SAVEDMOVIE
def save_to_db(mov):
    new_movie = SavedMovie(
        video_type = mov['vtype'],
        netflix_id = mov['nfid'],
        title = mov['title'],
    )
    try:
        db.session.add(new_movie)
        db.session.commit()
    except:
        db.session.rollback()

def get_data(audio, subs, start_year=1900, end_year=2020, offset=0, filter_movie=True, filter_series=True):
    end_year = end_year
    start_year = start_year
    limit = 12
    offset = offset
    audio = audio
    subtitle = subs

    # handle movie/series filter
    if filter_movie is True and filter_series is True:
        vtype = ''
    elif filter_movie is True and filter_series is False:
        vtype = '&type=movie'
    elif filter_movie is False and filter_series is True:
        vtype = '&type=series'
    else:
        raise

    # build API request args
    url = f'https://unogsng.p.rapidapi.com/search?end_year={end_year}&audiosubtitle_andor=and&start_year={start_year}&countrylist=78&limit={limit}&offset={offset}&audio={audio}&subtitle={subtitle}{vtype}'
    headers = {
        'x-rapidapi-host': API_HOST,
        'x-rapidapi-key': API_KEY,
        }

    try:
        response = requests.request("GET", url, headers=headers)
    except:
        return('api connection err')
    
    return(unescape(response.text))

def get_movie_detail(netflix_id):
    url = f'https://unogsng.p.rapidapi.com/title?netflixid={netflix_id}'
    headers = {
        'x-rapidapi-host': API_HOST,
        'x-rapidapi-key': API_KEY,
        }

    try:
        response = requests.request("GET", url, headers=headers)
    except:
        return('api connection err')
    
    response = json.loads(unescape(response.text))
    response = response['results'][0]

    movie_detail = {
        'title' : response['title'],
        'image_url' : response['img'],
        'synopsis' : response['synopsis'],
        'video_type' : response['vtype'],
        'netflix_id' : netflix_id,
    }
    
    return movie_detail