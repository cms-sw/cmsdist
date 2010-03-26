### RPM external py2-mongoengine 0.3
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://github.com/hmarr/mongoengine/tarball/v0.3
Requires: python py2-sphinx
%prep
#%setup -n mongoengine-%realversion
%setup -n hmarr-mongoengine-d314d88
%build
%install
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
python setup.py build
mv build/lib/* %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages


