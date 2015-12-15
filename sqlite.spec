### RPM external sqlite 3.8.11.1
Source: https://www.sqlite.org/2015/sqlite-autoconf-3081101.tar.gz

Requires: readline ncurses

%prep
%setup -n sqlite-autoconf-3081101

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking \
            CPPFLAGS="-I${READLINE_ROOT}/include -I${NCURSES_ROOT}/include" \
            CFLAGS="-L${READLINE_ROOT}/lib -L${NCURSES_ROOT}/lib"
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
