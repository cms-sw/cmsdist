### RPM external p5-perl-ostype 1.002
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Perl-OSType
Source: http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
