### RPM external nltk 2.0.4
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

Source0: https://pypi.python.org/packages/source/n/nltk/nltk-%{realversion}.tar.gz#md5=b17aad070ae9a094538e4b481409db09
Requires: python py2-yaml py2-numpy

%prep
%setup -n nltk-%{realversion}

%build
python setup.py build

%install
# install nltk
mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}

python setup.py install --skip-build --prefix=%{i} 
#exit 1

# download and install nltk data
# TODO: how to know this py2.6 prefix automatically?
cd %i/$PYTHON_LIB_SITE_PACKAGES/nltk-%{realversion}-py2.6.egg/nltk/
mkdir -p %{i}/%{_datadir}/nltk_data
python downloader.py -d %{i}/%{_datadir}/nltk_data words wordnet

find %i -name '*.egg-info' -exec rm {} \;

# get rid of /usr/bin/python
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'

