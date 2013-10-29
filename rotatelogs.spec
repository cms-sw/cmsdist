### RPM external rotatelogs 2.2.19
Source: http://archive.apache.org/dist/httpd/httpd-%realversion.tar.gz

%prep
%setup -n httpd-%realversion

%build
./configure --prefix=%i --disable-shared --with-included-apr 
perl -p -i -e 's/-l(expat|uuid)//g' \
  build/config_vars.mk \
  srclib/*/build/*.mk \
  srclib/*/*.pc \
  srclib/*/Makefile

cd srclib
make %makeprocesses

cd ../support
make %makeprocesses PROGRAMS=rotatelogs

%install
mkdir -p %i/bin
cp -p support/rotatelogs %i/bin
