### RPM external p5-digest-hmac 1.02
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Digest-HMAC
Source: http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-digest-sha1

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
