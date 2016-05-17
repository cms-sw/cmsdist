### RPM external sqlite 3.12.2
Source: https://www.sqlite.org/2016/sqlite-autoconf-3120200.tar.gz

Requires: readline ncurses

%prep
%setup -n sqlite-autoconf-3120200

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
