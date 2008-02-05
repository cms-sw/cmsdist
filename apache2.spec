### RPM external apache2 2.2.8
# See:
# http://httpd.apache.org/docs/2.2/install.html
# for instruction on how to configure.

# Required for https and compression support
Requires: openssl zlib expat uuid

# Can't figure out how to get rpm to stop complaining about this...
# should be in e2fsprogs-libs-1.39-7.slc4 ...
# but Requires uuid doesn't cover it
Provides: libcom_err.so.2

Source0: http://mirror.switch.ch/mirror/apache/dist/httpd/httpd-%realversion.tar.gz

%prep
%setup -n httpd-%realversion

%build
# See here:
#
# http://httpd.apache.org/docs/2.2/programs/configure.html#installationdirectories
#
# for configure options.

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
                        --with-openssl=$OPENSSL_ROOT \
                        --with-z=$ZLIB_ROOT \
			--with-expat=$EXPAT_ROOT \
			--with-uuid=$UUID_ROOT

                        

# %makeprocesses is for multiple compile processes -j X
make %makeprocesses

# Generates the dependencies-setup.{sh,csh} files so that
# sourcing init.{sh,csh} picks up also the environment of 
# dependencies.

rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
echo '#!/bin/sh' > %{i}/etc/profile.d/dependencies-setup.sh
echo '#!/bin/tcsh' > %{i}/etc/profile.d/dependencies-setup.csh
echo requiredtools `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
do
    case X$tool in
        Xdistcc|Xccache )
        ;;
        * )
            toolcap=`echo $tool | tr a-z- A-Z_`
            eval echo ". $`echo ${toolcap}_ROOT`/etc/profile.d/init.sh" >> %{i}/etc/profile.d/dependencies-setup.sh
            eval echo "source $`echo ${toolcap}_ROOT`/etc/profile.d/init.csh" >> %{i}/etc/profile.d/dependencies-setup.csh
        ;;
    esac
done

perl -p -i -e 's|\. /etc/profile\.d/init\.sh||' %{i}/etc/profile.d/dependencies-setup.sh
perl -p -i -e 's|source /etc/profile\.d/init\.csh||' %{i}/etc/profile.d/dependencies-setup.csh

find -type f | xargs perl -p -i -e "s|#\!.*perl(.*)|#!/usr/bin/env perl$1|" 

%install
make install

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
# Relocate the configuration files.
%{relocateConfig}/bin/apachectl
%{relocateConfig}/bin/apr-1-config
%{relocateConfig}/bin/apu-1-config
%{relocateConfig}/bin/apxs
%{relocateConfig}/bin/envvars
%{relocateConfig}/bin/envvars-std
%{relocateConfig}/build/apr_rules.mk
%{relocateConfig}/build/config.nice
%{relocateConfig}/build/config_vars.mk
%{relocateConfig}/build/libtool
%{relocateConfig}/conf/extra/httpd-autoindex.conf
%{relocateConfig}/conf/extra/httpd-dav.conf
%{relocateConfig}/conf/extra/httpd-manual.conf
%{relocateConfig}/conf/extra/httpd-multilang-errordoc.conf
%{relocateConfig}/conf/extra/httpd-ssl.conf
%{relocateConfig}/conf/extra/httpd-vhosts.conf
%{relocateConfig}/conf/httpd.conf
%{relocateConfig}/conf/original/extra/httpd-autoindex.conf
%{relocateConfig}/conf/original/extra/httpd-dav.conf
%{relocateConfig}/conf/original/extra/httpd-manual.conf
%{relocateConfig}/conf/original/extra/httpd-multilang-errordoc.conf
%{relocateConfig}/conf/original/extra/httpd-ssl.conf
%{relocateConfig}/conf/original/extra/httpd-vhosts.conf
%{relocateConfig}/conf/original/httpd.conf
%{relocateConfig}/include/ap_config_auto.h
%{relocateConfig}/include/ap_config_layout.h
%{relocateConfig}/lib/libapr-1.la
%{relocateConfig}/lib/libaprutil-1.la
%{relocateConfig}/lib/pkgconfig/apr-1.pc
%{relocateConfig}/lib/pkgconfig/apr-util-1.pc
