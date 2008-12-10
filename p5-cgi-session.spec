### RPM external p5-cgi-session 4.30
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn CGI-Session

Source: http://search.cpan.org/CPAN/authors/id/M/MA/MARKSTOS/%{downloadn}-%{realversion}.tar.gz
Requires:  p5-cgi

# Fake provides for optional backends
Provides:  perl(DBD::Pg)
Provides:  perl(DBI)
Provides:  perl(FreezeThaw)


%prep
%setup -n %downloadn-%{realversion}
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
