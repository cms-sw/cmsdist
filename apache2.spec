### RPM external apache2 2.2.14-gsi
Requires: openssl zlib expat uuid sqlite

# Silence dependencies which should have come via uuid from e2fsprogs
Provides: libcom_err.so.2
Provides: libcom_err.so.2()(64bit)

Source0: http://mirror.switch.ch/mirror/apache/dist/httpd/httpd-%realversion.tar.gz
Source1: http://www.apache.org/dist/httpd/httpd-%realversion.tar.gz
Source2: svn://vdt.cs.wisc.edu/svn/vdt/tags/vdt-2.0.0p18/Apache?scheme=https&module=Apache&output=/VDT-Apache-GSI.tgz
Patch0: apache2-verify-error

%prep
%setup -n httpd-%realversion
%patch0 -p0
gunzip -d -c < %_sourcedir/VDT-Apache-GSI.tgz |
  tar -xOf - 'Apache/nmi/GSI.patch' |
  patch -p0

%build
./configure --prefix=%i --with-mpm=prefork \
                        --enable-mods-shared=all \
                        --enable-so \
                        --with-included-apr \
                        --enable-cache \
                        --enable-proxy \
                        --enable-deflate \
                        --enable-disk-cache \
                        --enable-file-cache \
                        --enable-expires \
                        --enable-headers \
                        --enable-rewrite \
                        --enable-ssl \
                        --with-ssl=$OPENSSL_ROOT \
                        --with-z=$ZLIB_ROOT \
			--with-expat=$EXPAT_ROOT \
			--with-sqlite3=$SQLITE_ROOT \
			--with-uuid=$UUID_ROOT
make %makeprocesses
find -type f | xargs perl -p -i -e "s|#\!.*perl(.*)|#!/usr/bin/env perl$1|" 

%install
make install

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
%{relocateConfig}/bin/{apachectl,*-config,apxs,envvars*}
%{relocateConfig}/build/{libtool,*.mk}
%{relocateConfig}/conf/{original/,}{extra/,}*.conf
%{relocateConfig}/include/ap_config_*.h
%{relocateConfig}/lib/{*.la,pkgconfig/*.pc}
