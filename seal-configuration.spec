### RPM configuration seal-configuration 136
Source: none

Requires: gcc3-toolfile
Requires: cppunit-toolfile
Requires: qmtest-toolfile
Requires: oval-toolfile
Requires: valgrind-toolfile
Requires: pcre-toolfile
Requires: uuid-toolfile
Requires: root-toolfile
Requires: gsl-toolfile
Requires: clhep-toolfile
Requires: sockets-toolfile
Requires: x11-toolfile
Requires: python-toolfile
Requires: zlib-toolfile
Requires: bz2lib-toolfile
Requires: gccxml-toolfile

%prep
%build
%install
mkdir -p %{instroot}/configuration/CMS_%v
for x in %{instroot}/configuration/CMS_%v
do
echo $x
done
