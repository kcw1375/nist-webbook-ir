'''code to download and read IR spectra'''

import requests
from jcamp import jcamp_read
from bs4 import BeautifulSoup
import re

def get_jcampdx(molecule_id, index):
    '''
    molecule_id: a string, representing the molecule ID
    index: an int, representing the spectrum index for the molecule
    '''
    # get the IR spectrum JCAMP-DX data
    api_url=f'https://webbook.nist.gov/cgi/cbook.cgi?JCAMP={molecule_id}&amp;Index={index}&amp;Type=IR'
    response = requests.get(api_url)
    content = response.content.splitlines()
    content = [line.decode("utf-8") for line in content]
    return content

def parse_jcampdx(content):
    return jcamp_read(content)

def search(term):
    '''
    use the NIST webbook search feature to get molecule IDs

    Parameters:
    term: a string, the search term

    Returns:
    a dictionary keyed by molecule ID, with values of name and chemical formula 
    '''

    search_url = f'https://webbook.nist.gov/cgi/cbook.cgi?Name={term}&Units=SI&cIR=on'
    response = requests.get(search_url)

    # parse html to get search results
    soup = BeautifulSoup(response.content)
    results = dict()

    for result in soup.find('ol').find_all('li'):
        atag = result.find('a')
        # get id from the parameter in the href link
        # this regex extracts only the molecule id
        molecule_id = re.search('ID=.+?\&', atag['href']).group()[3:-1]
        molecule_name = atag.contents[0]
        formula = result.contents[1:] #todo: simplify formula
        results[molecule_id] = (molecule_name, formula)

    return results
