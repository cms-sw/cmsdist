### RPM external py2-pyxml 0.8.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: http://switch.dl.sourceforge.net/sourceforge/pyxml/PyXML-%{realversion}.tar.gz
Requires: python expat
Patch0: py2-pyxml-fix-as-keyword-usage-as-variable

%prep
%setup -n PyXML-%{realversion}
%patch0 -p0

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
for f in %i/bin/xmlproc_*; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
