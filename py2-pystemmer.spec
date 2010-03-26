### RPM external py2-pystemmer 1.0.1
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://snowball.tartarus.org/wrappers/PyStemmer-%{realversion}.tar.gz
Requires: python 
%prep
%setup -n PyStemmer-%realversion
#%patch0 -p1
%build
%install
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
python setup.py build
mv build/lib*/* %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages


