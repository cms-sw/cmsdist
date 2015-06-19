### RPM external p5-log-dispatch 2.26
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Log-Dispatch
Source: http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker p5-params-validate

# Provided by system perl
Provides:  perl(MIME::Lite)
Provides:  perl(Mail::Send)

# Fake provides for (hopefully) unneeded optional backends
Provides:  perl(Mail::Sender)
Provides:  perl(Mail::Sendmail)

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make %{makeprocesses}

%define drop_files %i/man
