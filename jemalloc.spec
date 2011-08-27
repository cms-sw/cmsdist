### RPM external jemalloc 2.2.2 
Source: http://www.canonware.com/download/jemalloc/jemalloc-%realversion.tar.bz2 

%prep
%setup -n %n-%{realversion}

%build
perl -p -i -e 's|-no-cpp-precomp||' configure
./configure --prefix %i

%install
make install
rm -rf %i/share
