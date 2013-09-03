### RPM external p5-params-validate 1.00
## INITENV +PATH PERL5LIB %i/lib/perl5
# Dummy comment: forcing the compiling for SLC6
%define downloadn Params-Validate
Source: http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-module-build p5-test-simple p5-attribute-handlers p5-extutils-cbuilder

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Build.PL --install_base %i
./Build

%install
./Build install

%define drop_files %i/man
