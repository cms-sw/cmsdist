### RPM external py2-setuptools 0.6c9
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://pypi.python.org/packages/source/s/setuptools/setuptools-%realversion.tar.gz
Requires: python
%prep
%setup -n setuptools-%realversion
%build
%install
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
python setup.py build
mv build/lib/* %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages


