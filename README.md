# NIST-Webbook-IR
A utility to search through IR spectra on the NIST chemistry webbook (https://webbook.nist.gov/chemistry/) and find matches for molecules based on absorption bands.

## Decoding Data
The NIST webbook renders IR spectra from a JCAMP-DX file, which is accessed via a GET request to a url of the form:
https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C57136&amp;Index=0&amp;Type=IR

The id in the parameter "JCAMP={}" represents the molecule ID as recorded by NIST.

The index number in the parameter "Index={}" may vary, as some molecules may have multiple IR recorded spectra in different phases, resolutions, and from different sources. 

The index numbers are not necessarily sequential, but it seems like the gas phase recorded by NIST Mass Spectrometry Data Center is usually index 0.

The file is encoded as base64 in the payload response, but simply clicking the link will let your browser handle downloading it.
