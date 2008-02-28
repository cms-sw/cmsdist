### RPM external p5-cgi 3.33
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn CGI.pm

Source: http://search.cpan.org/CPAN/authors/id/L/LD/LDS/%{downloadn}-%{v}.tar.gz

# Fake provides
Provides:  perl(FCGI)

%prep
%setup -n %downloadn-%v
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
