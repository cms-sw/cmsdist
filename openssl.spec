### RPM external openssl 0.9.8e__1.0.1
%define linver 0.9.8e
%define osxver 1.0.1
Source0: http://www.openssl.org/source/openssl-%osxver.tar.gz
Source1: http://cmsrep.cern.ch/cmssw/openssl-sources/%n-fips-%linver-usa.tar.bz2
Patch0: openssl-0.9.8e-22.el5_8.1-bundle
Patch1: openssl-x86-64-gcc420
# The following fixes CVE-2012-2110 (from http://cvs.openssl.org/chngview?cn=22431)
Patch2: openssl_patchset_22431

%prep
%ifos darwin
%setup -b 0 -n %n-%osxver
%else
%setup -b 1 -n %n-fips-%linver
%patch0 -p1
%patch1 -p1
%patch2 -p1
%endif

%build
# Looks like rpmbuild passes its own sets of flags via the
# RPM_OPT_FLAGS environment variable and those flags include
# -m64 (probably since rpmbuild processor detection is not
# fooled by linux32). A quick fix is to just set the variable
# to "" but we should probably understand how rpm determines
# those flags and use them for our own good.
export RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=generic"

cfg_opts="no-idea no-mdc2 no-rc5 no-ec no-ecdh no-ecdsa shared fipscanisterbuild"

case %cmsplatf in
  osx*)
    export KERNEL_BITS=64 # used by config to decide 64-bit build
    cfg_args="-DOPENSSL_USE_NEW_FUNCTIONS"
   ;;
  *)
    cfg_args="--with-krb5-flavor=MIT enable-krb5 fipscanisterbuild"
   ;;
esac

./config --prefix=%i $cfg_args enable-seed enable-tlsext enable-rfc3779 no-asm \
                     no-idea no-mdc2 no-rc5 no-ec no-ecdh no-ecdsa shared

make
%install
export RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=generic"

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
