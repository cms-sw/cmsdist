### RPM external pyminuit2 0.0.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: http://pyminuit2.googlecode.com/files/%{n}-%{realversion}.tar.gz
Requires: root 

Patch0: pyminuit2-cling

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
%install
python setup.py install --prefix=%i

#export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
