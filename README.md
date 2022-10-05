# NIST-Webbook-IR
A utility to search through IR spectra on the NIST chemistry webbook (https://webbook.nist.gov/chemistry/) and find matches for molecules based on absorption bands.

## Getting Started
First import the `spectrum` module to gain access to the functions.
To get a dictionary representing all the data within a specific IR spectrum, use:
```
data = spectrum.parse_jcampdx(spectrum.get_jcampdx('C71432', 0))
```
This data is the contents of the JCAMP-DX file with index 0 for molecule ID C71432 (Benzene).
The index number is important if there are multiple IR spectra recorded for a specific molecule, but usually leaving it on 0 is fine.

This data can then be plotted or otherwise manipulated using `matplotlib` or other libraries.


However, the more powerful feature is the ability to search and filter molecules by their IR absorption peaks.
```
search_results = spectrum.search('*amide')
desired_peaks = [
    PeakCriteria((500, 800)),
    PeakCriteria((2000, 2750), 0),
    PeakCriteria((1500, 1700), 1),
    ]
matching_spectra = dict()

for k in search_results:
    data = spectrum.parse_jcampdx(spectrum.get_jcampdx(k,0))
    peaks_found = spectrum.spectra_match(data, desired_peaks)
    
    if np.all(peaks_found):
        matching_spectra[k] = search_results[k]
```
This code selects amide molecules that have a peak of any size between 500-800 cm^-1, are flat between 2000-2750 cm^-1, and have their strongest peak between 1500-1700 cm^-1.

See the jupyter notebook provided within this repo for examples.

## ISSUES
This program depends on the jcamp package, but the pip release is currently broken.
Luckily, this is a simple fix.

Simply download the jcamp.py file from the github repo (https://github.com/nzhagen/jcamp) and replace the pip jcamp package by moving it to wherever your pip has downloaded jcamp (`pip show jcamp` to show its location).

## Decoding Data
The NIST webbook renders IR spectra from a JCAMP-DX file, which is accessed via a GET request to a url of the form:
https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C57136&amp;Index=0&amp;Type=IR

The id in the parameter "JCAMP={}" represents the molecule ID as recorded by NIST.

The index number in the parameter "Index={}" may vary, as some molecules may have multiple IR recorded spectra in different phases, resolutions, and from different sources. 

The index numbers are not necessarily sequential, but it seems like the gas phase recorded by NIST Mass Spectrometry Data Center is usually index 0.

The file is encoded as base64 in the payload response, but simply clicking the link will let your browser handle downloading it.
