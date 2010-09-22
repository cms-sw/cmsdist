### RPM external p5-apache-dbi 1.08
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define downloadn Apache-DBI
Source: http://search.cpan.org/CPAN/authors/id/A/AB/ABH/%downloadn-%realversion.tar.gz
Requires: p5-dbi p5-digest-sha1

%prep
%setup -n %downloadn-%realversion

%build
export LC_ALL=C
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
