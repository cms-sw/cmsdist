### RPM external p5-params-validate 0.91
# this is a comment to force it to build.
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn Params-Validate

Source: http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/%{downloadn}-%{realversion}.tar.gz

%prep
%setup -n %downloadn-%realversion
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
