### RPM external openssl 1.1.0g
%define openssl_tag %(echo %{realversion} | tr '.' '_')
Source0: https://github.com/%{n}/%{n}/archive/OpenSSL_%{openssl_tag}.tar.gz

%prep
%setup -b 0 -n openssl-OpenSSL_%{openssl_tag}

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
    cfg_args="no-zlib --openssldir=/etc/pki/tls fips no-ec2m no-gost no-srp"
    ;;
esac

export RPM_OPT_FLAGS

perl ./Configure ${target} ${cfg_args} enable-seed enable-rfc3779 no-asm \
                 no-idea no-mdc2 no-rc5 shared --prefix=%{i}

# Disable documenation
sed -ibak 's/^install:  *install_sw  *.*/install: install_sw/' Makefile

case "%{cmsplatf}" in
  *_aarch64_*|fc*|osx*)
    make depend
    ;;
esac

make all
make install

%install

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
