### RPM external ncurses 5.9
Source: http://ftp.gnu.org/pub/gnu/ncurses/ncurses-%realversion.tar.gz
%define keep_archives true
%define drop_files %i/lib/*.so

%prep
%setup -n ncurses-%realversion
%build
./configure --prefix %i --disable-shared --enable-static
make %makeprocesses CFLAGS="-O2 -fPIC" CXXFLAGS="-O2 -fPIC -std=c++11"
%install
make install
