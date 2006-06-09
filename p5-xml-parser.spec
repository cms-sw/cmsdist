### RPM external p5-xml-parser 2.34
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion/%perlarch
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn XML-Parser
Requires: expat
Source: http://mirror.switch.ch/ftp/mirror/CPAN/authors/id/M/MS/MSERGEANT/%{downloadn}-%{v}.tar.gz
%prep 
%setup -n %downloadn-%v
%build
which perl
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion \
                 EXPATLIBPATH=$EXPAT_ROOT/lib \
                 EXPATINCPATH=$EXPAT_ROOT/include
make
case $(uname)-$(uname -m) in
  Linux*)
    make test
esac
%install
make install
