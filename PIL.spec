### RPM external PIL 1.1.6
%define pythonv %(echo $PYTHON_VERSION |cut -d. -f1,2)
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION |cut -d. -f 1,2)/site-packages
Source: http://effbot.org/downloads/Imaging-%{v}.tar.gz
Requires: python libjpg zlib

%prep
%setup -n Imaging-%v
%build
python setup.py build
%install
python setup.py install --prefix=%i

