### RPM external py2-cryptography 2.4.2
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES} 

Requires: python openssl py2-cffi py2-asn1crypto py2-enum34 py2-idna py2-ipaddress py2-six

%define pip_name cryptography
%define PipPreBuild export LDFLAGS="-L${OPENSSL_ROOT}/lib"; \
                    export CFLAGS="-I${OPENSSL_ROOT}/include"

## IMPORT build-with-pip

#%define PipPostBuild \
#   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/*/*.py
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
