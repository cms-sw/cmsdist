### RPM external p5-xml-dom 1.44
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn XML-DOM
Source0: http://search.cpan.org/CPAN/authors/id/T/TJ/TJMATHER/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker
Provides: perl(LWP::UserAgent)
Provides: perl(XML::RegExp)

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
