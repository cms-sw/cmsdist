### RPM external openssl 1.0.2d
Source0: http://davidlt.web.cern.ch/davidlt/vault/openssl-1.0.2d-5675d07a144aa1a6c85f488a95aeea7854e86059.tar.bz2

# https://rt.openssl.org/Ticket/Display.html?id=3979&user=guest&pass=guest
Patch0: openssl-1.0.2d-pr3979
# We want to pick CA certificates from /etc/pki/tls (openssldir), but we
# cannot install to a standard system location
Patch1: openssl-1.0.2d-disable-install-openssldir

%prep
%setup -b 0 -n openssl-%{realversion}
%patch0 -p1
%patch1 -p1

# Disable documenation
sed -ibak 's/install: all install_docs install_sw/install: all install_sw/g' Makefile.org Makefile

case "%{cmsplatf}" in
  slc6*)
    # https://sourceware.org/glibc/wiki/Tips_and_Tricks/secure_getenv
    grep -H -R 'secure_getenv(' * | cut -d':' -f1 | sort -u | xargs -t -n 1 sed -ibak 's;secure_getenv;__secure_getenv;g'
    ;;
esac

%build

case "%{cmsplatf}" in
  slc6_amd64_*)
    RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing \
                   -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions \
                   -fstack-protector --param=ssp-buffer-size=4 -mtune=generic"
    ;;
  *_aarch64_*|fc*)
    RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
    ;;
esac

case "%{cmsplatf}" in
  osx*)         target=darwin64-x86_64-cc ;;
  *_aarch64_*)  target=linux-aarch64 ;;
  *_ppc64le_*)  target=linux-ppc64le ;;
  *_ppc64_*)    target=linux-ppc64 ;;
  *_amd64_*)    target=linux-x86_64 ;;
  *)            target=linux-generic64 ;;
esac

case "%{cmsplatf}" in
  osx*)
    cfg_args="-DOPENSSL_USE_NEW_FUNCTIONS"
    ;;
    *)
    cfg_args="--with-krb5-flavor=MIT --with-krb5-dir=/usr enable-krb5 no-zlib --openssldir=/etc/pki/tls fips no-ec2m no-gost no-srp"
    ;;
esac

export RPM_OPT_FLAGS

perl ./Configure ${target} ${cfg_args} enable-seed enable-tlsext enable-rfc3779 no-asm \
                 no-idea no-mdc2 no-rc5 shared --prefix=%{i}

case "%{cmsplatf}" in
  *_aarch64_*|fc*|osx*)
    make depend
    ;;
esac

make all

%install
case "%{cmsplatf}" in
  slc*_amd64_*)
    RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing \
                   -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions \
                   -fstack-protector --param=ssp-buffer-size=4 -mtune=generic"
    ;;
  *_aarch64_*|fc*)
    RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
    ;;
esac

export RPM_OPT_FLAGS

make install

rm -rf %{i}/lib/pkgconfig
# We remove archive libraries because otherwise we need to propagate everywhere
# their dependency on kerberos.
rm -rf %{i}/lib/*.a

sed -ideleteme -e 's;^#!.*perl;#!/usr/bin/env perl;' \
  %{i}/bin/c_rehash
find %{i} -name '*deleteme' -type f -print0 | xargs -0 rm -f

%post
%{relocateConfig}bin/c_rehash
%{relocateConfig}include/openssl/opensslconf.h
# bla bla
