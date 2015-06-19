### RPM external p5-log-dispatch-filerotate 1.19
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Log-Dispatch-FileRotate
Source: http://search.cpan.org/CPAN/authors/id/M/MA/MARKPF/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-log-dispatch

# provided by system perl
Provides: perl(Date::Manip)

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
