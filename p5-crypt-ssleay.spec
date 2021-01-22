### RPM external p5-crypt-ssleay 0.57
## INITENV +PATH PERL5LIB %i/lib/perl5
## NOCOMPILER
%define downloadn Crypt-SSLeay
Source: http://search.cpan.org/CPAN/authors/id/D/DL/DLAND/Crypt-SSLeay-0.57.tar.gz
Requires: p5-extutils-makemaker openssl
# As of 0.57-17 Crypt-SSLeay no longer ships the ca certs and uses the system ones in:
# Requires: /etc/pki/tls/certs/ca-bundle.crt

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
PERL_MM_USE_DEFAULT=1 perl Makefile.PL --lib=$OPENSSL_ROOT/lib INSTALL_BASE=%i
make pure_install

%define drop_files %i/man
%install
find %i -type f -name .packlist -exec rm -f {} ';'
find %i -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %i -type d -depth -exec rmdir {} 2>/dev/null ';'

# Set environment for openssl libs needed at runtime: 
mkdir -p %{i}/etc/profile.d
: > %{i}/etc/profile.d/dependencies-setup.sh
: > %{i}/etc/profile.d/dependencies-setup.csh

eval r=\$OPENSSL_ROOT
echo " . $r/etc/profile.d/init.sh" > %i/etc/profile.d/dependencies-setup.sh
echo " source $r/etc/profile.d/init.csh" > %i/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
