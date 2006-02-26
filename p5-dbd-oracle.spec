### RPM external p5-dbd-oracle 1.17
## INITENV +PATH PERL5LIB %i/lib/site_perl/$PERL_VERSION/%perlarch
%define perlarch %(perl -V | tr ',' '\\n' | grep arch | cut -d= -f2)
%define downloadn DBD-Oracle
Source: http://mirror.switch.ch/ftp/mirror/CPAN/authors/id/P/PY/PYTHIAN/%downloadn-%v.tar.gz
Requires: perl p5-dbi oracle
%prep
%setup -n %{downloadn}-%{v}
%build
perl Makefile.PL LIB=%i/lib/site_perl/$PERL_VERSION/
make
