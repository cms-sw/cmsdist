### RPM external ncurses 5.5
Requires: gcc-wrapper
Source: http://ftp.gnu.org/pub/gnu/ncurses/%{n}-%{v}.tar.gz

%build
## IMPORT gcc-wrapper
./configure --prefix=%i --with-shared --enable-symlinks
make

