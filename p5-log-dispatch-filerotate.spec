### RPM external p5-log-dispatch-filerotate 1.16
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn Log-Dispatch-FileRotate

Source: http://search.cpan.org/CPAN/authors/id/M/MA/MARKPF/%{downloadn}-%{realversion}.tar.gz
Requires:  p5-log-dispatch


# provided by system perl
Provides: perl(Date::Manip)

%prep
%setup -n %downloadn-%realversion
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
