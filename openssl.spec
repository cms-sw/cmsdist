### RPM external openssl 1.0.1r
Source: http://www.openssl.org/source/openssl-%realversion.tar.gz
Patch0: openssl-disable-install-openssldir

%prep
%setup -b 0 -n openssl-%realversion
%patch0 -p1

%build
case "%{cmsplatf}" in
  osx*)
    export KERNEL_BITS=64 # used by config to decide 64-bit build
    # OSX comes with the currently not supported Heimdal kerberos flavor
    cfg_args="no-krb5"
    ;;
  *)
    cfg_args="--with-krb5-flavor=MIT enable-krb5 --openssldir=/etc/pki/tls"
    ;;
esac

# Do not use the no-asm option for production servers as it implies
# in significant performance penalty.
./config --prefix=%{i} ${cfg_args} enable-seed enable-tlsext enable-rfc3779 \
                       no-idea no-mdc2 no-rc5 shared
#                       no-idea no-mdc2 no-rc5 no-ec no-ecdh no-ecdsa shared
make depend
make

%install
make install_sw # skips install_docs

# Make relocatable the scripts with hardcoded path to system perl
find %{i}/{bin,ssl/misc} -type f | xargs perl -p -i -e "s|#\!.*perl(.*)|#!/usr/bin/env perl$1|" 

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
