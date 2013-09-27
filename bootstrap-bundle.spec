### RPM external bootstrap-bundle 1.0
## INITENV SET MAGIC %{i}/share/misc/magic.mgc

%define keep_archives true
%define ismac   %(case %{cmsplatf} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isslc   %(case %{cmsplatf} in (slc*) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*|*_mic_*) echo 1 ;; (*) echo 0 ;; esac)
%define isarmv7 %(case %{cmsplatf} in (*armv7*) echo 1 ;; (*) echo 0 ;; esac)
%define isfc    %(case %{cmsplatf} in (fc*) echo 1 ;; (*) echo 0 ;; esac)
%if %ismac
%define soname dylib
%else
%define soname so
%endif

%define zlib_version            1.2.8
%define sqlite_version          3.7.17
%define popt_version            1.16
%define nss_version             3.14.3
%define nss_release_version     %(echo "%{nss_version}" | tr . _)_RTM
%define nspr_version            4.9.5
%define lua_version             5.1.5
%define libxml2_version         2.7.7
%define libxml2_downloadv       %(echo %{libxml2_version} | cut -d"_" -f1)
%define file_version            5.13
%define db4_version             4.4.20
%define bz2lib_version          1.0.5
%define openssl_version         1.0.1
%if %isslc
%define openssl_version         0.9.8e
%endif

%define openssl_flags1 -O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4
%if %isarmv7
%define openssl_flags2 -mtune=generic-armv7-a
%else
%define openssl_flags2 -mtune=generic
%endif
################# Sources ##############
#ZLIB
Source0:  http://zlib.net/zlib-%{zlib_version}.tar.gz

#SQLITE
Source1:  http://www.sqlite.org/2013/sqlite-autoconf-3071700.tar.gz

#POPT
Source2:  http://rpm5.org/files/popt/popt-%{popt_version}.tar.gz

#OPENSSL
%if %isslc
Source3:  http://cmsrep.cern.ch/cmssw/openssl-sources/openssl-fips-%{openssl_version}-usa.tar.bz2
%else
Source3:  http://www.openssl.org/source/openssl-%{openssl_version}.tar.gz
%endif

#NSS
Source4:  https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/NSS_%{nss_release_version}/src/nss-%{nss_version}.tar.gz

#NSPR
Source5:  https://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{nspr_version}/src/nspr-%{nspr_version}.tar.gz

#LUA
Source6:  http://www.lua.org/ftp/lua-%{lua_version}.tar.gz

#LIBXML2
Source7:  ftp://xmlsoft.org/libxml2/libxml2-%{libxml2_downloadv}.tar.gz

#FILE
Source8:  ftp://ftp.fu-berlin.de/unix/tools/file/file-%{file_version}.tar.gz

#DB$
Source9: http://download.oracle.com/berkeley-db/db-%{db4_version}.NC.tar.gz

#BZ2LIB
Source10: http://www.bzip.org/%{bz2lib_version}/bzip2-%{bz2lib_version}.tar.gz

############## Patches #############
#OPENSLL
Patch0: openssl-0.9.8e-rh-0.9.8e-12.el5_4.6
Patch1: openssl-x86-64-gcc420

#NSS
Patch2: nss-3.14.3-add-SQLITE-LIBS-DIR
Patch3: nss-3.14.3-add-ZLIB-LIBS-DIR-and-ZLIB-INCLUDE-DIR

#RPM
Patch4: rpm-4.8.0-case-insensitive-sources
Patch5: rpm-4.8.0-add-missing-__fxstat64
Patch6: rpm-4.8.0-fix-glob_pattern_p
Patch7: rpm-4.8.0-remove-strndup
Patch8: rpm-4.8.0-case-insensitive-fixes
Patch9: rpm-4.8.0-allow-empty-buildroot
Patch10: rpm-4.8.0-remove-chroot-check
Patch11: rpm-4.8.0-fix-missing-libgen
Patch12: rpm-4.8.0-fix-find-provides
Patch13: rpm-4.8.0-increase-line-buffer
Patch14: rpm-4.8.0-increase-macro-buffer
Patch15: rpm-4.8.0-improve-file-deps-speed
Patch16: rpm-4.8.0-fix-fontconfig-provides
Patch17: rpm-4.8.0-fix-find-requires-limit
Patch18: rpm-4.8.0-disable-internal-dependency-generator-libtool
Patch19: rpm-4.8.0-fix-arm

%prep
#ZLIB
%setup -T -b 0 -n zlib-%{zlib_version}

#SQLITE
%setup -T -b 1 -n sqlite-autoconf-3071700

#POPT
%setup -T -b 2 -n popt-%{popt_version}

#OPENSSL
%if %isslc
%setup -T -b 3 -n openssl-fips-%{openssl_version}
%patch0 -p1
%patch1 -p1
%else
%setup -T -b 3 -n openssl-%{openssl_version}
%endif

#NSS
%setup -T -b 4 -n nss-%{nss_version}
%patch2 -p1
%patch3 -p1

#NSPR
%setup -T -b 5 -n nspr-%{nspr_version}

#LUA
%setup -T -b 6 -n lua-%{lua_version}

#LIBXML2
%setup -T -b 7 -n libxml2-%{libxml2_downloadv}

#FILE
%setup -T -b 8 -n file-%{file_version}

#DB4
%setup -T -b 9 -n db-%{db4_version}.NC

#BZ2LIB
%setup -T -b 10 -n bzip2-%{bz2lib_version}
%if %ismac
sed -e 's/ -shared/ -dynamiclib/' \
    -e 's/ -Wl,-soname -Wl,[^ ]*//' \
    -e 's/libbz2\.so/libbz2.%{soname}/g' \
    < Makefile-libbz2_so > Makefile-libbz2_%{soname}
%endif

%build
#ZLIB
cd %{_builddir}/zlib-%{zlib_version}
case %{cmsplatf} in
   *_amd64_gcc4[56789]* )
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1 -msse3" \
     ./configure --prefix=%{i}/zlib
     ;;
   *_armv7hl_gcc4[56789]* )
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1" \
     ./configure --prefix=%{i}/zlib
     ;;
   * )
     ./configure --prefix=%{i}/zlib
     ;;
esac
make %{makeprocesses}
ln -s . include
ln -s . lib

#SQLITE
cd %{_builddir}/sqlite-autoconf-3071700
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i}/sqlite --disable-tcl --disable-static
make %{makeprocesses}

#NSPR
cd %{_builddir}/nspr-%{nspr_version}/mozilla/nsprpub
./configure --disable-static --prefix=%{i}/nspr --build=%{_build} --host=%{_host} \
%if %isamd64
--enable-64bit
%endif

make %{makeprocesses}

#POPT
cd %{_builddir}/popt-%{popt_version}
./configure --disable-static --disable-nls --prefix %{i}/popt --build="%{_build}" --host="%{_host}" CFLAGS="-fPIC" CXXFLAGS="-fPIC"
make

#LUA
cd %{_builddir}/lua-%{lua_version}
make -C src all MYLIBS="-ldl" MYCFLAGS="-fPIC -DLUA_USE_POSIX -DLUA_USE_DLOPEN"

#LIBXML2
cd %{_builddir}/libxml2-%{libxml2_version}
./configure --disable-static --prefix=%{i}/libxml2 --build="%{_build}" --host="%{_host}" --with-zlib="%{_builddir}/zlib-%{zlib_version}" --without-python
make %{makeprocesses}

#FILE
cd %{_builddir}/file-%{file_version}
./configure --prefix=%{i}/file --build="%{_build}" --host="%{_host}" --enable-static --disable-shared CFLAGS="-fPIC"
make %{makeprocesses}

#DB4
cd %{_builddir}/db-%{db4_version}.NC
mkdir obj
cd obj
../dist/configure --prefix=%{i}/db4 --build="%{_build}" --host="%{_host}" --disable-java --disable-tcl --disable-static
make %{makeprocesses}

#BZ2LIB
cd %{_builddir}/bzip2-%{bz2lib_version}
make %{makeprocesses} -f Makefile-libbz2_%{soname}

#OPENSSL
%if %isslc
cd %{_builddir}/openssl-fips-%{openssl_version}
%else
cd %{_builddir}/openssl-%{openssl_version}
%endif
export RPM_OPT_FLAGS="%{openssl_flags1} %{openssl_flags2}"
cfg_args="--with-krb5-flavor=MIT enable-krb5 fipscanisterbuild"
%if %ismac
    export KERNEL_BITS=64 # used by config to decide 64-bit build
    cfg_args="-DOPENSSL_USE_NEW_FUNCTIONS"
%endif
%if %isfc
    cfg_args="--with-krb5-flavor=MIT enable-krb5"
%endif
./config --prefix=%{i}/openssl ${cfg_args} enable-seed enable-tlsext enable-rfc3779 no-asm no-idea no-mdc2 no-rc5 no-ec no-ecdh no-ecdsa shared
case "%{cmsplatf}" in
  fc*|osx*) make depend ;;
esac
make
RPM_OPT_FLAGS=
KERNEL_BITS=

#NSS
cd %{_builddir}/nss-%{nss_version}
export NSPR_INCLUDE_DIR="%{_builddir}/nspr-%{nspr_version}/mozilla/nsprpub/dist/include/nspr"
export NSPR_LIB_DIR="%{_builddir}/nspr-%{nspr_version}/mozilla/nsprpub/dist/lib"
export USE_SYSTEM_ZLIB=1
export ZLIB_INCLUDE_DIR="%{_builddir}/zlib-%{zlib_version}/include"
export ZLIB_LIBS_DIR="%{_builddir}/zlib-%{zlib_version}/lib"
export NSS_USE_SYSTEM_SQLITE=1
export SQLITE_INCLUDE_DIR="%{_builddir}/sqlite-autoconf-3071700"
export SQLITE_LIBS_DIR="%{_builddir}/sqlite-autoconf-3071700/.lib"
%if %isamd64
export USE_64=1
%endif

make -C ./mozilla/security/coreconf
make -C ./mozilla/security/dbm
make -C ./mozilla/security/nss

%install
#ZLIB
cd %{_builddir}/zlib-%{zlib_version}
make install
rm -rf %{i}/zlib/share

#SQLITE
cd %{_builddir}/sqlite-autoconf-3071700
make install
rm -rf %{i}/lib/pkgconfig

#NSPR
cd %{_builddir}/nspr-%{nspr_version}/mozilla/nsprpub
make install

#POPT
cd %{_builddir}/popt-%{popt_version}
make install
rm -rf {%i}/popt/share

#LUA
cd %{_builddir}/lua-%{lua_version}
make install INSTALL_TOP=%{i}/lua
rm -rf %{i}/lua/{share,man}

#LIBXML2
cd %{_builddir}/libxml2-%{libxml2_version}
make install
rm -rf %{i}/libxml2/share/{man,doc,gtk-doc}
rm -rf %{i}/libxml2/lib/pkgconfig
rm -rf %{i}/libxml2/lib/*.{l,}a

#FILE
cd %{_builddir}/file-%{file_version}
make install
rm -rf %{i}/file/share/man

#DB4
cd %{_builddir}/db-%{db4_version}.NC/obj
make install
rm -rf %{i}/db4/docs

#BZ2LIB
cd %{_builddir}/bzip2-%{bz2lib_version}
make install PREFIX=%{i}/bz2lib
# For bzip2 1.0.5, the library appears to retain the name libbz2.so.1.0.4
# rather than libbz2.so.1.0.5 as one would expect, so use this "tmpversion"
# instead of realversion
%define tmpversion 1.0.4
cp libbz2.%{soname}.%{tmpversion} %{i}/bz2lib/lib
ln -s libbz2.%{soname}.%{tmpversion} %{i}/bz2lib/lib/libbz2.%{soname}
ln -s libbz2.%{soname}.%{tmpversion} %{i}/bz2lib/lib/libbz2.%{soname}.`echo %{tmpversion} | cut -d. -f 1,2`
ln -s libbz2.%{soname}.%{tmpversion} %{i}/bz2lib/lib/libbz2.%{soname}.`echo %{tmpversion} | cut -d. -f 1`
ln -sf bzdiff %{i}/bz2lib/bin/bzcmp
ln -sf bzgrep %{i}/bz2lib/bin/bzegrep
ln -sf bzgrep %{i}/bz2lib/bin/bzfgrep
ln -sf bzmore %{i}/bz2lib/bin/bzless
rm -rf %{i}/bz2lib/man

#OPENSSL
%if %isslc
cd %{_builddir}/openssl-fips-%{openssl_version}
%else
cd %{_builddir}/openssl-%{openssl_version}
%endif
export RPM_OPT_FLAGS="%{openssl_flags1} %{openssl_flags2}"
make install
rm -rf %{i}/openssl/lib/pkgconfig
rm -rf %{i}/openssl/lib/*.a
rm -rf %{i}/openssl/ssl/man
perl -p -i -e "s|^#!.*perl|#!/usr/bin/env perl|" %{i}/openssl/ssl/misc/CA.pl %{i}/openssl/ssl/misc/der_chop %{i}/openssl/bin/c_rehash

#NSS
cd %{_builddir}/nss-%{nss_version}
rm -rf %{i}/nss/lib/libsoftokn3*
rm -rf %{i}/nss/lib/libsql*
install -d %{i}/nss/include/nss3
install -d %{i}/nss/lib
find mozilla/dist/public/nss -name '*.h' -exec install -m 644 {} %{i}/nss/include/nss3 \;
find . -path "*/mozilla/dist/*.OBJ/lib/*.%{soname}" -exec install -m 755 {} %{i}/nss/lib \;

#Mobve all libs/bin in top level lib/bin
mkdir %{i}/install
for tool in bz2lib  db4  file libxml2  lua  nspr  nss  openssl  popt  sqlite  zlib ; do
  rsync -r --links --ignore-existing %{i}/${tool}/ %{i}/install/
  rm -rf %{i}/${tool}
done
mv %{i}/install/* %{i}
rm -rf %{i}/install
find %{i}/bin -type f -perm -a+x -exec %strip {} \;
find %{i}/lib -type f -perm -a+x -exec %strip {} \;

mv %{i}/share/aclocal %{i}/share/aclocal.backup
rm -rf mv %{i}/share/man
rm -rf mv %{i}/ssl
mkdir %{i}/tmp
mv %{i}/lib/lib{lua,magic}.a %{i}/tmp
rm -f %{i}/lib/*.{l,}a
mv %{i}/tmp/lib* %{i}/lib/
rm -rf %{i}/tmp

%post
%{relocateConfig}bin/xml2-config
%{relocateConfig}lib/xml2Conf.sh
