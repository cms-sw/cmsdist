### RPM external p5-xml-parser 2.34
## INITENV +PATH PERL5LIB $P5_XML_PARSER_ROOT/lib/site_perl/$PERL_VERSION/$(uname -m)-$(uname -s | tr 'A-Z' 'a-z')
%define downloadn XML-Parser
Requires: perl expat
Source: http://mirror.switch.ch/ftp/mirror/CPAN/authors/id/M/MS/MSERGEANT/%{downloadn}-%{v}.tar.gz
%prep 
%setup -n %downloadn-%v
%build
which perl
perl Makefile.PL PREFIX=%{i}
make
make test
%install
make install
