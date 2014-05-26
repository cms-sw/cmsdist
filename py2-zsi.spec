### RPM external py2-zsi 2.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://switch.dl.sourceforge.net/sourceforge/pywebsvcs/ZSI-%{realversion}.tar.gz
Requires: python py2-pyxml

%prep 
%setup -n ZSI-%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
for f in %i/bin/wsdl2*; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
