### RPM external py3-pycurl 7.43.0.3
## IMPORT build-with-pip3

Requires: curl openssl

%define PipPreBuild export PYCURL_SSL_LIBRARY=openssl
%define PipBuildOptions --global-option="--with-openssl" --global-option="--openssl-dir=${OPENSSL_ROOT}"
