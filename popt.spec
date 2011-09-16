### RPM external popt 1.15
Source: http://rpm5.org/files/%n/%n-%realversion.tar.gz

%build
./configure --disable-shared --enable-static --disable-nls \
            --prefix %i \
            CFLAGS="-fPIC" \
            CXXFLAGS="-fPIC"  
make
%install
make install

# Strip libraries, we are not going to debug them.
find %i/lib -type f -perm -a+x -exec strip {} \;

# Don't need archive libraries.
rm -f %i/lib/*.{l,}a

# Look up documentation online.
rm -rf %i/share
