### RPM external py2-ipython 0.10
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
%define realname %(echo "%{n}" | cut -d- -f 2-)
Source: http://archive.ipython.org/release/%{realversion}/%{realname}-%{realversion}.tar.gz
Requires: python

%define drop_files %{i}/share

%prep
%setup -n %{realname}-%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix=%{i}
egrep -r -l '^#!.*python' %{i} | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %{i} -name '*.egg-info' -exec rm {} \;
