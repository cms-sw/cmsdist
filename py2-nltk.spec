### RPM external py2-nltk 2.0.4
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

Source0: https://pypi.python.org/packages/source/n/nltk/nltk-%{realversion}.tar.gz#md5=b17aad070ae9a094538e4b481409db09
Requires: python py2-yaml py2-numpy
BuildRequires: py2-setuptools

%prep
%setup -n nltk-%{realversion}

%build
python setup.py build

%install
python setup.py install --skip-build --prefix=%{i} --single-version-externally-managed --record=/dev/null

# Use the downloader script to install nltk data.
# This is terrible for the configuration management, but nltk
# does not distribute the data files in a single, versioned, tarball.
cd %i/$PYTHON_LIB_SITE_PACKAGES/nltk/
mkdir -p %{i}/nltk_data
export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}
python downloader.py -d %{i}/nltk_data words wordnet stopwords

find %i -name '*.egg-info' -exec rm {} \;
# get rid of /usr/bin/python
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'

%post
# add NLTK_DATA into init so it would be available afterwards
echo "export NLTK_DATA='${CMS_INSTALL_PREFIX}/%{pkgrel}/nltk_data'" >> ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/profile.d/init.sh
echo "setenv NLTK_DATA '${CMS_INSTALL_PREFIX}/%{pkgrel}/nltk_data'" >> ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/profile.d/init.csh
