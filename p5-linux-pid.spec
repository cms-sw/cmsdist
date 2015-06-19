### RPM external p5-linux-pid 0.04
## INITENV +PATH PERL5LIB %i/lib/perl5
# Dummy comment: forcing the compiling for SLC6
%define downloadn Linux-Pid
Source: http://search.cpan.org/CPAN/authors/id/R/RG/RGARCIA/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
