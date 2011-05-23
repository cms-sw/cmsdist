### RPM external py2-yajl 0.3.5
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: https://github.com/rtyler/py-yajl/zipball/v%{realversion}
Requires: python yajl

%prep
%setup -n rtyler-py-yajl-*

%build
rm -rf yajl
ln -s $YAJL_ROOT yajl
python setup.py build_ext --inplace

%install
python setup.py install --prefix=%i
# --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
