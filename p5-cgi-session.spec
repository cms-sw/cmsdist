### RPM external p5-cgi-session 4.46
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn CGI-Session
Source: http://search.cpan.org/CPAN/authors/id/M/MA/MARKSTOS/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-cgi

# Fake provides for optional backends
Provides:  perl(DBD::Pg)
Provides:  perl(DBI)
Provides:  perl(FreezeThaw)
Provides:  perl(Test::More)

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
