### RPM external p5-dbd-mysql 3.0002
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn DBD-mysql

Source: http://search.cpan.org/CPAN/authors/id/C/CA/CAPTTOFU/%downloadn-%v.tar.gz
Requires: p5-dbi mysql

%prep
%setup -n %{downloadn}-%{v}

%build
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
