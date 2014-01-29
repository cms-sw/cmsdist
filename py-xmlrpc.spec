### RPM external py-xmlrpc 0.8.8.2
%define pythonv $(echo $PYTHON_VERSION | cut -d. -f 1,2)
%define pydir $(which python| python -c "import sys,os; version=sys.version[:3];path='/'+reduce(lambda x,y: x+y+'/',sys.stdin.readline().split('/')[:-2]);print path")
%define bindir %pydir/bin
%define sitedir %pydir/lib/python%pythonv/site-packages
## INITENV +PATH PYTHONPATH %{i}/lib/python%pythonv/site-packages

Summary: xmlrpc for Python
Source0: http://switch.dl.sourceforge.net/sourceforge/py-xmlrpc/%n-%v.tar.gz
Patch0: py-xmlrpc-parse4
Patch1: py-xmlrpc-0.8.8.2-info
Group: Development/Libraries
Vendor: Shilad Sen <shilad.sen@sourcelight.com>
Url: http://sourceforge.net/projects/py-xmlrpc/
Requires: gcc python

%description
This kit contains an implementation of the xmlrpc protocol written in C and
wrapped up in python.

%prep
%setup -n %n-%v
%patch0 -p0
%patch1 -p0

%build
export CFLAGS="-I%pydir/include/"
python setup.py build

%install
python setup.py install --prefix=%i
