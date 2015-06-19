### RPM external p5-attribute-handlers 0.91
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Attribute-Handlers
Source: http://search.cpan.org/CPAN/authors/id/S/SM/SMUELLER/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
