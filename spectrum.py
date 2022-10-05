'''code to download and read IR spectra'''

import requests
from jcamp import jcamp_read
from bs4 import BeautifulSoup
import re
import numpy as np

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
    soup = BeautifulSoup(response.content, features='html.parser')
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

def spectra_match(data, peaks):
    '''
    defines a metric for how good a "match" an IR spectra to some desired absorption bands

    Parameters:
    data: a dictionary with 'x', 'y' keys, representing the IR spectrum to observe
    peaks: a list of PeakCriteria, representing the properties of peaks that the IR spectra should have
    
    Returns:
    a list of bools, where each element i represents if a peak satisfying the peak criteria was found in the region described by peaks[i]
    '''
    spectrum = np.array([data['x'], data['y']])
    # print(spectrum.shape)
    # first get the background radiation level by computing the median
    background = np.median(spectrum[1])
    # now determine the threshold in deviation for absorption, above which we'll consider a peak
    threshold = np.std(spectrum[1])/3 # let's use 1/3 standard deviation
    # print(background, threshold)

    # plot is either absorbance or transmittance, which will determine how we calculate peaks
    # thus, check yunits
    is_absorbance = (data.get('yunits') == 'ABSORBANCE')

    matches = []
    for peak in peaks:
        limits = (peak.range[0] < spectrum[0]) * (spectrum[0] < peak.range[1])

        # handle case where the spectrum does not even contain the wavelengths
        if not np.any(limits):
            matches.append(False)
            continue

        # if is an absorbance plot
        if is_absorbance:
            # we use the naive method of checking the max within these limits and seeing if that's above the threshold
            max_y = np.max(spectrum[1, limits])
            # print(max_y)
            matches.append(max_y > background + threshold)
        else: # if is a transmittance plot
            # instead check the minimum
            min_y = np.min(spectrum[1, limits])
            # print(min_y)
            matches.append(min_y < background - threshold)

        
    return matches

class PeakCriteria:
    '''
    this class is effectively a struct that represents the search criteria for absorption peaks
    '''
    def __init__(self, range, strength=None):
        '''
        Parameters:
        range: a 2-tuple representing the wavenumber range the peak should be found within, [0] is the lower bound, [1] is the upper bound
        strength: float between 0 and 1, representing the desired relative strength of the peak compared to other peaks.
            If None, then the peak only needs to be present, and not satisfy this relative strength condition
        '''
        self.range = range
        self.strength = strength 
