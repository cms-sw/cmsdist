### RPM external gmp 4.2.1
Source: ftp://mirrors.kernel.org/gnu/%n/%n-%realversion.tar.gz

%install
make install
find %i/lib -type f -perm -a+x -exec strip {} \;
rm -f %i/lib/*.{l,}a
rm -fr %i/info
