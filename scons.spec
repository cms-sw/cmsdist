### RPM external scons 1.2.0
## INITENV +PATH PYTHONPATH %i/lib/%n-%realversion
Source: http://prdownloads.sourceforge.net/scons/scons-%realversion.tar.gz
Requires: python

%prep
%setup -n scons-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
%define drop_files %i/man
