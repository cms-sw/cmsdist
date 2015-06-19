### RPM external p5-apache-dbi 1.08
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Apache-DBI
Source: http://search.cpan.org/CPAN/authors/id/A/AB/ABH/%downloadn-%realversion.tar.gz
Requires: p5-extutils-makemaker p5-dbi p5-digest-sha1

%prep
%setup -n %downloadn-%realversion

%build
export LC_ALL=C
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
