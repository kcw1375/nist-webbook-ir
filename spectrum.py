'''code to download and read IR spectra'''

import requests

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
