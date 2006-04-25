### RPM external mod_python 3.2.8
Source: http://apache.mirror.testserver.li/httpd/modpython/%{n}-%{v}.tgz
## INITENV +PATH PYTHONPATH %{i}/lib
## INITENV CMD ln -sf $MOD_PYTHON_ROOT/lib/mod_python.so $APACHE_ROOT/modules
Requires: python apache
%build
./configure --prefix=%{i} \
            --with-python=$PYTHON_ROOT/bin/python \
            --with-apxs=$APACHE_ROOT/bin/apxs
make

%install
mkdir -p %i/lib
install -m 0644 src/mod_python.so %i/lib
cp -rp lib/python/mod_python %i/lib

%files
%i
