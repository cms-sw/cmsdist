### RPM external py2-simplejson 1.9.2
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://pypi.python.org/packages/source/s/simplejson/simplejson-%{realversion}.tar.gz
Requires: python
%prep
%setup -n simplejson-%realversion
#%patch0 -p1
%build
%install
# we need simple json only for python 2.5 and earlier, but for python 2.6 and higher
if  [ -z `echo $PYTHON_VERSION | egrep "2.6|3."` ]; then
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
python setup.py build
pwd
mv build/lib*/* %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
fi

