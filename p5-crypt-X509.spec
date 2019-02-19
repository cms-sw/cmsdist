### RPM external p5-crypt-X509 0.51
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Crypt-X509
Source: https://cpan.metacpan.org/authors/id/A/AJ/AJUNG/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-convert-asn1

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
