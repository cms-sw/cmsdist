### RPM cms py3-dbs3-pycurl 3.17.9
## IMPORT build-with-pip3
Requires: py3-pycurl

# PycurlClient has different setup scripts
%define patchsrc mv setup4pypi.py setup.py
