### RPM external whoosh 2.4.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

%global mod_name Whoosh

Source0: https://pypi.python.org/packages/source/W/%{mod_name}/%{mod_name}-%{realversion}.tar.gz

Requires: python
#BuildRequires:  python2-devel python-setuptools python-nose python-sphinx
BuildRequires: py2-sphinx

%prep
%setup -n Whoosh-%{realversion}
wget http://python-distribute.org/distribute_setup.py %{i}/${PYTHON_LIB_SITE_PACKAGES}/Whoosh-%{realversion}/
# append distribute to top of setup.py

%build
python setup.py build
#sphinx-build docs/source docs/html
#rm -f docs/html/.buildinfo
#rm -rf docs/html/.doctrees

%check
%{__python} setup.py test

%install
# install nltk
mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}

python setup.py install -O1 --skip-build --prefix=%{i} 
#exit 1

find %i -name '*.egg-info' -exec rm {} \;
# get rid of /usr/bin/python
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'

