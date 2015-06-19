### RPM external p5-poe-component-child 1.39
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn POE-Component-Child
Source: http://search.cpan.org/CPAN/authors/id/E/EC/ECALDER/%{downloadn}-%{realversion}.tar.gz
Patch0: p5-poe-component-child
Requires: p5-extutils-makemaker p5-poe

%prep
%setup -n %downloadn-%realversion
%patch0 -p0

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
