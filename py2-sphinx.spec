### RPM external py2-sphinx 1.3.5
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define sphinx_rtd_theme_version 0.1.9
%define alabaster_version 0.7.8
%define babel_version 2.3.4
%define snowballstemmer_version 1.2.1

Source0: http://pypi.python.org/packages/source/S/Sphinx/Sphinx-%realversion.tar.gz
Source1: http://github.com/snide/sphinx_rtd_theme/archive/%sphinx_rtd_theme_version.tar.gz
Source2: http://github.com/bitprophet/alabaster/archive/%alabaster_version.tar.gz
Source3: http://github.com/python-babel/babel/archive/%babel_version.tar.gz
Source4: http://pypi.python.org/packages/source/s/snowballstemmer/snowballstemmer-%snowballstemmer_version.tar.gz
Requires: python py2-docutils py2-jinja py2-pygments py2-setuptools py2-six py2-pytz

%prep
%setup -T -b 0 -n Sphinx-%realversion
%setup -D -T -b 1 -n sphinx_rtd_theme-%sphinx_rtd_theme_version
%setup -D -T -b 2 -n alabaster-%alabaster_version
%setup -D -T -b 3 -n babel-%babel_version
%setup -D -T -b 4 -n snowballstemmer-%snowballstemmer_version

%build
for d in ../Sphinx-* ../sphinx_rtd_theme-* ../alabaster-* ../babel-* ../snowballstemmer-*; do
  cd $d
  python setup.py build
done

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
for d in ../Sphinx-* ../sphinx_rtd_theme-* ../alabaster-* ../babel-* ../snowballstemmer-*; do
  cd $d
  if [ $d != ../snowballstemmer-* ]; then
    python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
  else
    PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
    python setup.py install --prefix=%i
  fi
done
for f in %i/bin/sphinx-*; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
