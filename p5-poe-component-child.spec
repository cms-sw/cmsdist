### RPM external p5-poe-component-child 1.39
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn POE-Component-Child

Source: http://search.cpan.org/CPAN/authors/id/E/EC/ECALDER/%{downloadn}-%{realversion}.tar.gz
Requires:  p5-poe

%prep
%setup -n %downloadn-%realversion
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
