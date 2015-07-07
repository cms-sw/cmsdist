### RPM external p5-digest-sha1 2.13
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Digest-SHA1
Source: http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
