### RPM external py3-pycurl 7.45.1
## IMPORT build-with-pip3

Requires: curl
%define PipBuildOptions --global-option="--with-openssl"
%define pip_name pycurl
%define PipPreBuild export PYCURL_SSL_LIBRARY=openssl

