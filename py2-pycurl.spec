### RPM external py2-pycurl 7.43.0.1
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define PipBuildOptions --global-option="--with-openssl" --global-option="--openssl-dir=${OPENSSL_ROOT}" 
%define pip_name pycurl
Requires: curl openssl

## IMPORT build-with-pip

