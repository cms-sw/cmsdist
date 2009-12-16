### RPM external p5-log-log4perl 1.16
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn Log-Log4perl

Source:  http://search.cpan.org/CPAN/authors/id/M/MS/MSCHILLI/%{downloadn}-%{realversion}.tar.gz
Requires: p5-log-dispatch p5-log-dispatch-filerotate

# Provided by system perl
Provides:  perl(XML::DOM)

# Fake provides for optional backends
Provides:  perl(RRDs)
Provides:  perl(DBI)


%prep
%setup -n %downloadn-%realversion
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
