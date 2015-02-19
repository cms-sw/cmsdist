### RPM external py2-yajl 0.3.5
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://github.com/rtyler/py-yajl/zipball/v%{realversion}
Patch: py2-yajl-nogit
Requires: python yajl

%prep
%setup -n rtyler-py-yajl-4f25a9b
%patch

%build
rm -rf yajl
ln -s $YAJL_ROOT yajl
python setup.py build_ext --inplace

%install
python setup.py install --prefix=%i
# --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
