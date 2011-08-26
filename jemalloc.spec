### RPM external jemalloc 2.2.2 
Source: http://www.canonware.com/download/jemalloc/jemalloc-%realversion.tar.bz2 

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix %i

%install
make install
strip %i/lib/*
rm -rf %i/share
