### RPM external py2-pycurl 7.43.0.3
## IMPORT build-with-pip

%define PipBuildOptions --global-option="--with-openssl" --global-option="--openssl-dir=${OPENSSL_ROOT}"
%define pip_name pycurl
%define PipPreBuild export PYCURL_SSL_LIBRARY=openssl

Requires: curl openssl
