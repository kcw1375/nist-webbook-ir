'''code to download and read IR spectra'''

import requests

def get_jcampdx(molecule_id, index):
    '''
    molecule_id: a string, representing the molecule ID
    index: an int, representing the spectrum index for the molecule
    '''
    # get the IR spectrum JCAMP-DX data
    return requests.get(f'https://webbook.nist.gov/cgi/cbook.cgi?JCAMP={molecule_id}&amp;Index={index}&amp;Type=IR').text
