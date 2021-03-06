import requests
import json
from html import unescape
from os import environ
import requests_cache
import importlib

# set local development config vars if folder exists
dev_config = importlib.util.find_spec('config')
if dev_config is not None:
    from config.api_config import API_HOST, API_KEY
else:
    API_HOST = environ.get('UNOGS_API_HOST')
    API_KEY = environ.get('UNOGS_API_KEY')

# cache api requests for 24 hours
requests_cache.install_cache(cache_name='unogs_cache', backend='sqlite', expire_after=86400)

def get_data(audio, subs, start_year=1900, end_year=2020, offset=0, filter_movie=True, filter_series=True, results_per_page=12):
    end_year = end_year
    start_year = start_year
    limit = results_per_page
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

    # build API request
    url = f'https://unogsng.p.rapidapi.com/search?end_year={end_year}&audiosubtitle_andor=and&orderby=rating&start_year={start_year}&countrylist=78&limit={limit}&offset={offset}&audio={audio}&subtitle={subtitle}{vtype}'
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
        'imdbid' : response['imdbid'],
        'netflix_id' : netflix_id,
    }
    return movie_detail