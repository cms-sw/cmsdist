### RPM external py2-sphinx 0.6.4
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://pypi.python.org/packages/source/S/Sphinx/Sphinx-%realversion.tar.gz
Requires: python 
%prep
%setup -n Sphinx-%realversion
%build
%install
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
export PYTHONPATH=$PYTHONPATH:%i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
python setup.py build
python setup.py install --prefix=%i


