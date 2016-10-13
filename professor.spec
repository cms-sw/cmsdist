### RPM external professor 1.0.0
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: http://www.hepforge.org/archive/professor/professor-%{realversion}.tar.gz

Requires: py2-numpy py2-scipy pyminuit2 py2-matplotlib
BuildRequires: py2-setuptools
%prep
%setup -n professor-%{realversion}

%build

%install
export MPLCONFIGDIR=$PWD
./setup.py --distutils install
mkdir %i/bin
cp bin/* %i/bin
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
mkdir -p %i/lib/python$PYTHONV/site-packages
cp -r build/lib/professor %i/lib/python$PYTHONV/site-packages 

