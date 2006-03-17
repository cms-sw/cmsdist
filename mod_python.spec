### RPM external mod_python 3.2.8
Source: http://apache.mirror.testserver.li/httpd/modpython/%{n}-%{v}.tgz
Requires: python apache
%build
./configure --prefix=%{i} \
            --with-python=$PYTHON_ROOT/bin/python \
            --with-apxs=$APACHE_ROOT/bin/apxs
make %makeprocesses
