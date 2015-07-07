### RPM external p5-log-log4perl 1.26
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Log-Log4perl
Source:  http://search.cpan.org/CPAN/authors/id/M/MS/MSCHILLI/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-log-dispatch p5-log-dispatch-filerotate p5-xml-dom

# Fake provides for optional backends
Provides:  perl(RRDs)
Provides:  perl(DBI)


%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
