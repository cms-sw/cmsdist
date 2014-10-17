### RPM external p5-apache24-modssl 0.08
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Apache2-ModSSL
Source: http://search.cpan.org/CPAN/authors/id/O/OP/OPI/%downloadn-%realversion.tar.gz
Requires: mod_perl24 p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
export LC_ALL=C
perl Makefile.PL INSTALL_BASE=%i
make PASTHRU_INC=-I$MOD_PERL24_ROOT/include

%define drop_files %i/man
