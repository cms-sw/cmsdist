### RPM external p5-convert-asn1 0.27
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Convert-ASN1
Source: https://cpan.metacpan.org/authors/id/G/GB/GBARR/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
