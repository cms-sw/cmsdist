### RPM external ncurses 6.0-20151128
Source: ftp://invisible-island.net/ncurses/current/ncurses-%{realversion}.tgz
%define keep_archives true
%define drop_files %{i}/lib/*.so

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix="%{i}" \
            --build="%{_build}" \
            --host="%{_host}" \
            --disable-shared \
            --enable-static \
            --without-debug \
            --without-ada \
            --without-manpages \
            --enable-termcap

make %{makeprocesses} CFLAGS="-O2 -fPIC" CXXFLAGS="-O2 -fPIC -std=c++11"

%install
make install
