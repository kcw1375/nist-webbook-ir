# NIST-Webbook-IR
A utility to search through IR spectra on the NIST chemistry webbook (https://webbook.nist.gov/chemistry/) and find matches for molecules based on absorption bands.

## Decoding Data
The NIST webbook renders IR spectra from a JCAMP-DX file, which is accessed via a GET request to a url of the form:
https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C57136&amp;Index=0&amp;Type=IR
The file is encoded as base64 in the payload response.
