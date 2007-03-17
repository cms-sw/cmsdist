### RPM external py2-sqlobject 0.8.0
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages

%define distname SQLObject-%v
Source: http://cheeseshop.python.org/packages/source/S/SQLObject/%{distname}.tar.gz
Patch0: patch-setup
Requires: python

%prep
%setup -n %{distname}
%patch0
%build
%install
python setup.py install --prefix=%i
perl -p -i -e "s|#\!.*python|#!/usr/bin/env python|" %i/bin/sqlobject-admin

