### RPM external rotatelogs 2.2.25
Source: http://archive.apache.org/dist/httpd/httpd-%realversion.tar.gz

%prep
%setup -n httpd-%realversion
perl -p -i -e 's/-no-cpp-precomp//' srclib/apr/configure

%build
./configure --prefix=%i --with-included-apr --disable-shared
cd srclib
make %makeprocesses

cd ../support
make %makeprocesses PROGRAMS=rotatelogs

%install
mkdir -p %i/bin
cp -p support/rotatelogs %i/bin
