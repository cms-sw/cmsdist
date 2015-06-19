### RPM external p5-ipc-cmd 0.72
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn IPC-Cmd
Source: http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-module-load-conditional

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
