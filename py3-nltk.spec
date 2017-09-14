### RPM external py3-nltk 3.2.4
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

#Source0: https://pypi.python.org/packages/source/n/nltk/nltk-%{realversion}.tar.gz#md5=b17aad070ae9a094538e4b481409db09
#Source0: https://pypi.python.org/packages/13/ce/cba8bf82c8ab538d444ea4ab6f4eb1d80340c7b737d7a8d1f08b429fccae/nltk-%{realversion}.tar.gz#md5=4cbb8fd444402cf1847c47ff79dcd917
Source0: https://pypi.python.org/packages/cd/c2/858e0708b497116ae45cf5c6b1f66984ac60729c61e49df6c1c0b808d1e4/nltk-3.2.4.tar.gz
Requires: python3 py3-yaml py3-numpy py3-six
BuildRequires: py3-setuptools

%prep
%setup -n nltk-%{realversion}

%build
export PYTHON3_ROOT
export PY3_NUMPY_ROOT
#export LDFLAGS="-L$PYTHON3_ROOT/lib $LDFLAGS"
#pver=`python3 -V | awk '{print $2}' | cut -d . -f 1,2`
#export PYTHONPATH=$PY3_NUMPY_ROOT/lib/python$pver/site-packages:$PYTHONPATH
python3 setup.py build

%install
export PYTHON3_ROOT
export PY3_NUMPY_ROOT
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
#PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python3 setup.py install --skip-build --prefix=%{i} --single-version-externally-managed --record=/dev/null

# Use the downloader script to install nltk data.
# This is terrible for the configuration management, but nltk
# does not distribute the data files in a single, versioned, tarball.
cd %i/$PYTHON_LIB_SITE_PACKAGES/nltk/
mkdir -p %{i}/nltk_data
#export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}
#python3 downloader.py -d %{i}/nltk_data words wordnet stopwords
cd %{i}/nltk_data
curl -O https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/stopwords.zip
unzip stopwords.zip
curl -O https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/words.zip
unzip words.zip
curl -O https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet.zip
unzip wordnet.zip

find %i -name '*.egg-info' -exec rm {} \;
# replace all instances of #!/path/bin/python into proper format
for f in `find %i -type f`; do
    if [ -f $f ]; then
        perl -p -i -e 's{.*}{#!/usr/bin/env python3} if $. == 1 && m{#!.*/bin/python.*}' $f
    fi
done

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
