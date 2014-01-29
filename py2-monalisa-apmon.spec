### RPM external py2-monalisa-apmon 2.2.1
%define pythonv $(echo $PYTHON_VERSION | cut -d. -f 1,2)
%define pydir $(which python| python -c "import sys,os; version=sys.version[:3];path='/'+reduce(lambda x,y: x+y+'/',sys.stdin.readline().split('/')[:-2]);print path")
%define bindir %pydir/bin
%define sitedir %pydir/lib/python%pythonv/site-packages
## INITENV +PATH PYTHONPATH %{i}/lib

Summary: Python client to send monitoring data to MonaLISA
Group: Development/Libraries
Vendor: Conrad Steenberg <conrad@hep.caltech.edu>
Source: http://monalisa.cacr.caltech.edu/download/apmon/ApMon_py-%v.tar.gz
Requires: python

%description
A pure Python module that can be used to send monitoring variables to a
MonaLISA monitoring server via UDP.

%prep
%setup -n ApMon_py-%v

%build

%install
mkdir -p %i/lib
cp apmon.py %i/lib
cp ProcInfo.py %i/lib
cp Logger.py %i/lib

%files
%i
