### RPM external p5-compress-zlib 1.34
## INITENV +PATH PERL5LIB %i/lib/site_perl/$PERL_VERSION/%perlarch
%define perlarch %(perl -e 'use Config; print $Config{archname}')
%define downloadn Compress-Zlib

Requires: perl-virtual
Requires: zlib
Source: http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/%{downloadn}-%{v}.tar.gz
%prep
%setup -n %downloadn-%v
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL LIB=%i/lib/site_perl/$PERL_VERSION PREFIX=%i \
  LIB=$ZLIB_ROOT INCLUDE=$ZLIB_ROOT/include
make
