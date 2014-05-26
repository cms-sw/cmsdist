### RPM external apache2 2.2.25gsi
%define apversion %(echo %realversion | sed 's/gsi.*$//')
Requires: openssl zlib expat libuuid sqlite pcre

Source0: http://archive.apache.org/dist/httpd/httpd-%apversion.tar.gz
Patch0: apache2-verify-error
Patch1: apache2-ssl-report-cert
Patch2: apache2-gsi

%prep
%setup -n httpd-%apversion
perl -p -i -e 's/-no-cpp-precomp//' srclib/apr/configure
%patch0 -p0
%patch1 -p0
%patch2 -p0

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
                        --with-pcre=$PCRE_ROOT \
                        --with-ssl=$OPENSSL_ROOT \
                        --with-z=$ZLIB_ROOT \
			--with-expat=$EXPAT_ROOT \
			--with-sqlite3=$SQLITE_ROOT \
			--with-uuid=$LIBUUID_ROOT \
			--without-pgsql
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
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Strip libraries, we are not going to debug them.
%define strip_files %i/{bin,lib,modules}

# Look up documentation online; don't need archive libraries.
%define drop_files %i/{manual,man} %i/lib/{apr*/,}*.{l,}a

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
%{relocateConfig}/bin/{apachectl,*-config,apxs,envvars*}
%{relocateConfig}/build/{libtool,*.mk}
%{relocateConfig}/conf/{original/,}{extra/,}*.conf
%{relocateConfig}/include/ap_config_*.h
