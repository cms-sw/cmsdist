### RPM external p5-monalisa-apmon 2.2.17
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion

Summary: The MonaLisa ApMon client code

Source: http://monalisa.cern.ch/download/apmon/%{downloadn}-%{v}.tar.gz
Url: http://monalisa.cern.ch/

%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn ApMon_perl
%description
The Perl ApMon client for Monalisa.
%prep
%setup -n %downloadn-%v
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
