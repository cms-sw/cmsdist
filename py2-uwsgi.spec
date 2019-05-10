### RPM external py2-uwsgi 2.0.18
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Requires: python openssl libuuid pcre
Provides: libcrypto.so.10(libcrypto.so.10)(64bit)
Provides: libssl.so.10(libssl.so.10)(64bit)

%define pip_name uwsgi

## IMPORT build-with-pip

#%define PipPostBuild \
#   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/*/*.py
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
