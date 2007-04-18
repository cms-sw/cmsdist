### RPM external p5-compress-zlib 1.34
Requires: gcc-wrapper
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn Compress-Zlib

Requires: zlib
Source: http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/%{downloadn}-%{v}.tar.gz
%prep
%setup -n %downloadn-%v
%build
## IMPORT gcc-wrapper
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion INCLUDE=$ZLIB_ROOT/include
make
#
