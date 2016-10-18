### RPM external sqlite 3.15.0
Source: http://sqlite.org/2016/sqlite-autoconf-3150000.tar.gz

Requires: readline

%prep
%setup -n sqlite-autoconf-3150000

%build
./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking \
            CPPFLAGS="-I${READLINE_ROOT}/include" \
            CFLAGS="-L${READLINE_ROOT}/lib"
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
