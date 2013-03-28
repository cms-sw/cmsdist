### RPM external popt 1.15
Source: http://rpm5.org/files/%n/%n-%realversion.tar.gz

%build
./configure --disable-static --disable-nls \
            --prefix %i \
            CFLAGS="-fPIC" \
            CXXFLAGS="-fPIC"  
make
%define drop_files %i/share
