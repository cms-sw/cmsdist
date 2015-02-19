### RPM external py2-nltk 2.0.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

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

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
# add NLTK_DATA into init so it would be available afterwards
echo "export NLTK_DATA='${CMS_INSTALL_PREFIX}/%{pkgrel}/nltk_data'" >> ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/profile.d/init.sh
echo "setenv NLTK_DATA '${CMS_INSTALL_PREFIX}/%{pkgrel}/nltk_data'" >> ${RPM_INSTALL_PREFIX}/%{pkgrel}/etc/profile.d/init.csh
