### RPM external py2-pycrypto 2.0.1 
%define downloadn pycrypto
Requires: python gmp
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}$(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
Source: http://www.amk.ca/files/python/crypto/%downloadn-%v.tar.gz 
Patch: py2-pycrypto-setup

%prep
%setup -n %downloadn-%v
%patch0 -p0
%build
%install
python setup.py install --prefix=%i
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "^#\!.*python.*" %i | cut -d: -f1`
