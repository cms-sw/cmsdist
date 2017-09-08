### RPM external py3-sphinx 1.6.3
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define sphinx_rtd_theme_version 0.1.9
%define alabaster_version 0.7.8
%define babel_version 2.3.4
%define snowballstemmer_version 1.2.1

#Source0: http://pypi.python.org/packages/source/S/Sphinx/Sphinx-%realversion.tar.gz
Source0: https://pypi.python.org/packages/10/91/ceb2e0d763e0c626f7afd7e3272a5bb76dd06eed1f0b908270ea31984062/Sphinx-%realversion.tar.gz
Source1: http://github.com/snide/sphinx_rtd_theme/archive/%sphinx_rtd_theme_version.tar.gz
Source2: http://github.com/bitprophet/alabaster/archive/%alabaster_version.tar.gz
Source3: http://github.com/python-babel/babel/archive/%babel_version.tar.gz
Source4: http://pypi.python.org/packages/source/s/snowballstemmer/snowballstemmer-%snowballstemmer_version.tar.gz
Requires: python3 py3-docutils py3-jinja py3-pygments py3-setuptools py3-six py3-pytz

%prep
%setup -T -b 0 -n Sphinx-%realversion
%setup -D -T -b 1 -n sphinx_rtd_theme-%sphinx_rtd_theme_version
%setup -D -T -b 2 -n alabaster-%alabaster_version
%setup -D -T -b 3 -n babel-%babel_version
%setup -D -T -b 4 -n snowballstemmer-%snowballstemmer_version

%build
for d in ../Sphinx-* ../sphinx_rtd_theme-* ../alabaster-* ../babel-* ../snowballstemmer-*; do
  cd $d
  python3 setup.py build
done

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
for d in ../Sphinx-* ../sphinx_rtd_theme-* ../alabaster-* ../babel-* ../snowballstemmer-*; do
  cd $d
  if [ $d != ../snowballstemmer-* ]; then
    python3 setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
  else
    PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
    python3 setup.py install --prefix=%i
  fi
done
for f in %i/bin/sphinx-*; do perl -p -i -e 's{.*}{#!/usr/bin/env python3} if $. == 1 && m{#!.*/bin/python}' $f; done
for f in %i/bin/py*; do perl -p -i -e 's{.*}{#!/usr/bin/env python3} if $. == 1 && m{#!.*/bin/python}' $f; done
