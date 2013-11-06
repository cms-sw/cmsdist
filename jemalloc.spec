### RPM external jemalloc 3.4.1
Source: http://www.canonware.com/download/jemalloc/jemalloc-%realversion.tar.bz2 

%prep
%setup -n %n-%{realversion}

%build
perl -p -i -e 's|-no-cpp-precomp||' configure
./configure --prefix %i

%define drop_files %i/share
