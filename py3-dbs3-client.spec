### RPM cms py3-dbs3-client 4.0.4
## IMPORT build-with-pip3
Requires: py3-pycurl py3-dbs3-pycurl

# DBSClient has different setup scripts
%define patchsrc mv setupPypi.py setup.py
