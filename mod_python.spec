### RPM external mod_python 3.2.10
# See http://www.modpython.org/live/current/doc-html/installation.html

Requires:  apache2 python

Source0: http://apache.mirror.testserver.li/httpd/modpython/mod_python-%realversion.tgz

%pre
%setup -n mod_python-%realversion

./configure --with-python=$PYTHON_ROOT/bin/python --with-apxs=$APACHE2_ROOT/bin/apxs --with-max-locks=32

%build
%install
