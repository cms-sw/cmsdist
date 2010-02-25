### RPM external p5-mail-rfc822-address 0.3
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn Mail-RFC822-Address

Source: http://search.cpan.org/CPAN/authors/id/P/PD/PDWARREN/%{downloadn}-%{realversion}.tar.gz

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
