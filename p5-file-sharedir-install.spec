### RPM external p5-file-sharedir-install 0.13
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn File-ShareDir-Install
Source: https://cpan.metacpan.org/authors/id/E/ET/ETHER/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
