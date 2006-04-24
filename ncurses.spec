### RPM external ncurses 5.5
Source: http://ftp.gnu.org/pub/gnu/ncurses/%{n}-%{v}.tar.gz

%build
./configure --prefix=%i
make

