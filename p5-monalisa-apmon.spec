### RPM external p5-monalisa-apmon 2.2.18
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn ApMon_perl
Source: http://monalisa.cern.ch/download/apmon/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
