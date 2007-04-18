### RPM external py2-zsi 1.7
Requires: gcc-wrapper
%define pythonv `echo $PYTHON_VERSION | cut -d. -f 1,2`
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
Source: http://switch.dl.sourceforge.net/sourceforge/pywebsvcs/ZSI-%{v}.tar.gz
Requires: python

%prep 
%setup -n ZSI-%v
%build
## IMPORT gcc-wrapper
./setup.py build
%install
./setup.py install --prefix=%{i}
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/wsdl2dispatch.py %{i}/bin/wsdl2py.py
