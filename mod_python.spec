### RPM external mod_python 3.2.8

%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %{i}/lib/python%{pythonv}
## INITENV CMD ln -sf $MOD_PYTHON_ROOT/lib/mod_python.so $APACHE_ROOT/modules

Source: http://apache.osuosl.org/httpd/modpython/%{n}-%{v}.tgz
Requires: python apache


%build
./configure --prefix=%{i} \
            --with-python=$PYTHON_ROOT/bin/python \
            --with-apxs=$APACHE_ROOT/bin/apxs

make

cd dist
python setup.py build

%install

mkdir -p %i/lib
cp src/mod_python.so %i/lib

cd dist
python setup.py install --prefix=%i

mv %{i}/lib/python%{pythonv}/site-packages/mod_python \
  %{i}/lib/python%{pythonv}

rm -rf %{i}/lib/python%{pythonv}/site-packages

