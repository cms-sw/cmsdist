### RPM external py2-pyxml 0.8.4
%define pythonv `echo $PYTHON_VERSION | cut -d. -f 1,2`
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
Source: http://switch.dl.sourceforge.net/sourceforge/pyxml/PyXML-%{realversion}.tar.gz
Requires: python expat

%prep
%setup -n PyXML-%{realversion}
%build
./setup.py build
%install
./setup.py install --prefix=%{i}
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/xmlproc_parse %{i}/bin/xmlproc_val
