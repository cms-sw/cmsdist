### RPM external cppunit 1.10.2-XXXX
Source0: http://switch.dl.sourceforge.net/sourceforge/%n/%n-%realversion.tar.gz
Source1: http://spi.cvs.cern.ch:8180/cgi-bin/spi.cgi/*checkout*/Components/UnitTesting/Tools/CppUnit/CppUnit_testdriver.cpp?rev=1.1

%prep
%setup -n %n-%realversion

%build
./configure --prefix=%i
make %makeprocesses
%install
make install
cp %_sourcedir/CppUnit_testdriver.cpp* %i/include/CppUnit_testdriver.cpp
%post
%{relocateConfig}/bin/cppunit-config
%{relocateConfig}/lib/libcppunit.la
