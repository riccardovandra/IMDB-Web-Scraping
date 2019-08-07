# import request, BeautifulSoup and Pandas Libraries
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from IPython.core.display import clear_output
from time import sleep
from time import time
from random import randint
from warnings import warn

# url to scrape
years_url = [str(i) for i in range(2000, 2020)]
pages = [str(50*i+1) for i in range(0, 4)]
basic_url = 'https://www.imdb.com/search/title/?year='


# declare list variables

names = []
years = []
imdb_ratings = []
metascores = []
votes = []

# Preparing the monitoring of the loop
start_time = time()
requests = 0

# extract data from different movie container

# For every year in interval 2000, 2018
for year_url in years_url:
    # For every page in interval 1 - 4
    for page in pages:
        # Make the request
        response = get(basic_url + year_url + '&start=' + page)

        # Pause the loop
        sleep(randint(8, 15))

        # Monitor requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request: {}; Frequency: {} requests/s'.format(requests,
                                                             requests/elapsed_time))
        clear_output(wait=True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status Code: {}'.format(
                requests, response.status_code))

        # Break the loop if there are more than 72 requests
        if requests > 72:
            warn('Number of requests was greater than expected.')
            break

        # Parse content of the request using BeautifulSoup (html.parser is Python's built-in function to parse html content)
        html_soup = BeautifulSoup(response.text, 'html.parser')

        # find all the movie containers in the specific page
        movie_containers = html_soup.find_all(
            'div', class_='lister-item mode-advanced')

        # scrape all the movies in the specific page & append infos to lists
        for container in movie_containers:
            # if the movie has a metascore then extract
            if container.find('div', class_='ratings-metascore') is not None:
                # The name
                name = container.h3.a.text
                names.append(name)
                # The year
                year = container.h3.find(
                    'span', class_='lister-item-year').text
                years.append(year)
                # The imdb rating
                imdb_rating = float(container.strong.text)
                imdb_ratings.append(imdb_rating)
                # The metascore
                metascore = int(container.find(
                    'span', class_='metascore').text)
                metascores.append(metascore)
                # Votes
                vote = int(container.find('span', attrs={
                    'name': 'nv'})['data-value'])
                votes.append(vote)
