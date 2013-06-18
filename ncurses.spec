### RPM external ncurses 5.5
Source: http://ftp.gnu.org/pub/gnu/ncurses/%{n}-%{realversion}.tar.gz

%build
./configure --prefix=%i --with-shared --enable-symlinks
make

