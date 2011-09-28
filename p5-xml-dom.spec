### RPM external p5-xml-dom 1.4.4
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn XML-DOM
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make
