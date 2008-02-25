### RPM external mod_python 3.2.10
# See http://www.modpython.org/live/current/doc-html/installation.html

Requires:  apache2 python

Source0: http://apache.mirror.testserver.li/httpd/modpython/mod_python-%realversion.tgz

%prep
%setup -n mod_python-%realversion

./configure --with-python=$PYTHON_ROOT/bin/python --with-apxs=$APACHE2_ROOT/bin/apxs --with-max-locks=32

%build
make

%install
make install

mkdir -p %i/conf
cat << \EOF > %i/conf/mod_python.conf
LoadModule mod_python %i/modules/mod_python.so
# Additional configuration bits go here.
EOF

# By default mod_python.so and is moved to the
# $APACHE2_ROOT/modules directory, which
# is bad for us handling multiple versions in a rpm.
mkdir -p %i/modules
mv $APACHE2_ROOT/modules/mod_python.so %i/modules

%post
%{relocateConfig}conf/mod_python.conf
