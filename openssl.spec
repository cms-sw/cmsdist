### RPM external openssl 0.9.8e__1.0.1
%define slc_version 0.9.8e
%define generic_version 1.0.1
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
Provides: libcrypt.so.1(GLIBC_2.14)(64bit)
%endif
Source0: http://www.openssl.org/source/%{n}-%{generic_version}.tar.gz
Source1: http://cmsrep.cern.ch/cmssw/openssl-sources/%{n}-fips-%{slc_version}-usa.tar.bz2
Patch0: openssl-0.9.8e-rh-0.9.8e-12.el5_4.6
Patch1: openssl-x86-64-gcc420

%define ismac %(case %{cmsplatf} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isfc %(case %{cmsplatf} in (fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isslc %(case %{cmsplatf} in (slc*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%if %ismac
%setup -b 0 -n %{n}-%{generic_version}
%endif
%if %isfc
%setup -b 0 -n %{n}-%{generic_version}
%endif
%if %isslc
%setup -b 1 -n %{n}-fips-%{slc_version}
%patch0 -p1
%patch1 -p1
%endif

%build
# Looks like rpmbuild passes its own sets of flags via the
# RPM_OPT_FLAGS environment variable and those flags include
# -m64 (probably since rpmbuild processor detection is not
# fooled by linux32). A quick fix is to just set the variable
# to "" but we should probably understand how rpm determines
# those flags and use them for our own good.
%if "%mic" == "true"
RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing \
               -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions \
               --param=ssp-buffer-size=4"
%else
RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing \
               -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions \
               -fstack-protector --param=ssp-buffer-size=4"
%endif

case "%{cmsplatf}" in
  *armv7*)
    RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -mtune=generic-armv7-a"
    ;;
  *)
    RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -mtune=generic"
    ;;
esac

export RPM_OPT_FLAGS

case "%{cmsplatf}" in
  *_mic_*)
    cfg_args="fipscanisterbuild -mmic"
   ;;
  osx*)
    export KERNEL_BITS=64 # used by config to decide 64-bit build
    cfg_args="-DOPENSSL_USE_NEW_FUNCTIONS"
    ;;
  fc*)
    cfg_args="--with-krb5-flavor=MIT enable-krb5"
    ;;
  *)
    cfg_args="--with-krb5-flavor=MIT enable-krb5 fipscanisterbuild"
    ;;
esac

./config --prefix=%{i} ${cfg_args} enable-seed enable-tlsext enable-rfc3779 no-asm \
                       no-idea no-mdc2 no-rc5 no-ec no-ecdh no-ecdsa shared

case "%{cmsplatf}" in
  fc*|osx*)
    make depend
    ;;
esac

%if "%mic" == "true"
sed -i -e 's| gcc *$|icc|g' Makefile
%endif
sed -i -e 's|#SET_X=|SET_X=|' Makefile.shared
make

%install
%if "%mic" == "true"
RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing \
               -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions \
               --param=ssp-buffer-size=4"
%else
RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing \
               -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions \
               -fstack-protector --param=ssp-buffer-size=4"
%endif

case "%{cmsplatf}" in
  *armv7*)
    RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -mtune=generic-armv7-a"
    ;;
  *)
    RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -mtune=generic"
    ;;
esac

export RPM_OPT_FLAGS

make install

rm -rf %{i}/lib/pkgconfig
# We remove archive libraries because otherwise we need to propagate everywhere
# their dependency on kerberos.
rm -rf %{i}/lib/*.a

# MacOSX is case insensitive and the man page structure has case sensitive logic
case %cmsplatf in
  osx* ) 
    rm -rf %{i}/ssl/man
    ;;
esac
perl -p -i -e "s|^#!.*perl|#!/usr/bin/env perl|" %{i}/ssl/misc/CA.pl %{i}/ssl/misc/der_chop %{i}/bin/c_rehash
