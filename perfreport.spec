### RPM cms perfreport 2.0.0
## INITENV SET PERFREPORT_PATH %i/share/perfreport
Source: http://cmsdoc.cern.ch/~moserro/scr/perfreport-%realversion.tar.gz
Requires: py2-matplotlib py2-numpy python zlib expat openssl bz2lib db4 gdbm openssl libxml2

%install
make install
mkdir -p %{i}/etc/profile.d
(echo "source $PYTHON_ROOT/etc/profile.d/init.sh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_MATPLOTLIB_ROOT/etc/profile.d/init.sh"; \
 echo "source $PY2_NUMPY_ROOT/etc/profile.d/init.sh"; \
 echo "source $LIBXML2_ROOT/etc/profile.d/init.sh"; \
 echo "source $DB4_ROOT/etc/profile.d/init.sh"; \
 echo "source $GDBM_ROOT/etc/profile.d/init.sh"; \
 echo "source $ZLIB_ROOT/etc/profile.d/init.sh"; \
 echo "source $BZ2LIB_ROOT/etc/profile.d/init.sh"; \
 echo "source $EXPAT_ROOT/etc/profile.d/init.sh"; \
 echo "source $GCC_ROOT/etc/profile.d/init.sh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.sh" ) > %{i}/etc/profile.d/dependencies-setup.sh

(echo "source $PYTHON_ROOT/etc/profile.d/init.csh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_MATPLOTLIB_ROOT/etc/profile.d/init.csh"; \
 echo "source $PY2_NUMPY_ROOT/etc/profile.d/init.csh"; \
 echo "source $LIBXML2_ROOT/etc/profile.d/init.csh"; \
 echo "source $DB4_ROOT/etc/profile.d/init.csh"; \
 echo "source $GDBM_ROOT/etc/profile.d/init.csh"; \
 echo "source $ZLIB_ROOT/etc/profile.d/init.csh"; \
 echo "source $BZ2LIB_ROOT/etc/profile.d/init.csh"; \
 echo "source $EXPAT_ROOT/etc/profile.d/init.csh"; \
 echo "source $GCC_ROOT/etc/profile.d/init.csh"; \
 echo "source $OPENSSL_ROOT/etc/profile.d/init.csh" ) > %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

