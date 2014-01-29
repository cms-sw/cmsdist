### RPM external p5-libwww-perl 1.41-CMS19
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn libwww-perl
%define downloadv 5.805

Requires: p5-uri

## FIXME: we fake the existance of these to remove rpm complaining about needing it.
Provides: perl(Authen::NTLM)
Provides: perl(HTML::Entities) 
Provides: perl(HTTP::GHTTP)
Provides: perl(Win32)

Source: http://cpan.mirror.solnet.ch/authors/id/G/GA/GAAS/%{downloadn}-%{downloadv}.tar.gz
%prep 
%setup -n %downloadn-%downloadv
%build
which perl
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
%install
make install
#
