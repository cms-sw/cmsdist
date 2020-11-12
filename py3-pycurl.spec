### RPM external py3-pycurl 7.43.0.3
## IMPORT build-with-pip3

Requires: curl
%define PipBuildOptions --global-option="--with-openssl"
%define pip_name pycurl
%define PipPreBuild export PYCURL_SSL_LIBRARY=openssl

