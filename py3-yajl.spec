### RPM external py3-yajl 0.3.5
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://github.com/rtyler/py-yajl/zipball/v%{realversion}
Patch: py2-yajl-nogit
Requires: python3 yajl

%prep
%setup -n rtyler-py-yajl-4f25a9b
%patch

%build
rm -rf yajl
ln -s $YAJL_ROOT yajl
export PYTHON3_ROOT
export LDFLAGS="-L$PYTHON3_ROOT/lib $LDFLAGS"
python3 setup.py build_ext --inplace

%install
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python3 setup.py install --prefix=%i
# --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;

# replace all instances of #!/path/bin/python into proper format
%py3PathRelocation

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
%addDependency

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
