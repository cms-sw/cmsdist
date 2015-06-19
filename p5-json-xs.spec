### RPM external p5-json-xs 2.3
## INITENV +PATH PERL5LIB %i/lib/perl5
# Dummy comment: forcing the compiling for SLC6...
%define downloadn JSON-XS
Source: http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-common-sense

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
