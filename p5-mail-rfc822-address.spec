### RPM external p5-mail-rfc822-address 0.3
# Dummy comment: forcing the compiling for SLC6...
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Mail-RFC822-Address
Source: http://search.cpan.org/CPAN/authors/id/P/PD/PDWARREN/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
