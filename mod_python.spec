### RPM external mod_python 3.2.8

%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %{i}/lib/python%{pythonv}
## INITENV CMD ln -sf $MOD_PYTHON_ROOT/lib/mod_python.so $APACHE_ROOT/modules

Source: http://apache.mirror.testserver.li/httpd/modpython/%{n}-%{v}.tgz
Requires: python apache


%build
./configure --prefix=%{i} \
            --with-python=$PYTHON_ROOT/bin/python \
            --with-apxs=$APACHE_ROOT/bin/apxs

cd dist
python setup.py build

%install
cd dist
python setup.py install --prefix=%i
