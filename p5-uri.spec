### RPM external p5-uri 1.35-CMS19
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn URI
Source: http://mirror.switch.ch/ftp/mirror/CPAN/authors/id/G/GA/GAAS/%downloadn-%{realversion}.tar.gz

# Let's remove the dependency on ISBN stuff...
Provides: perl(Business::ISBN)

%prep
%setup -n %downloadn-%{realversion}
%build
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
%install
make install
#
