### RPM external p5-cgi 3.33
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn CGI.pm
Source: http://search.cpan.org/CPAN/authors/id/L/LD/LDS/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

# Fake provides
Provides:  perl(FCGI)

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
