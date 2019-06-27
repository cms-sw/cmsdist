### RPM external p5-sort-key 1.25
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn Sort-Key

Source: http://search.cpan.org/CPAN/authors/id/S/SA/SALVA/%{downloadn}-%{v}.tar.gz

%prep
%setup -n %downloadn-%v

%build
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
# bla bla
