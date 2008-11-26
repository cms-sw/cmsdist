### RPM external p5-crypt-blowfish 2.10
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn Crypt-Blowfish

Source:  http://search.cpan.org/CPAN/authors/id/D/DP/DPARIS/%{downloadn}-%{realversion}.tar.gz

%prep
%setup -n %downloadn-%realversion
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
