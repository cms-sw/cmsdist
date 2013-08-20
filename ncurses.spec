### RPM external ncurses 5.9
Source: http://ftp.gnu.org/pub/gnu/%{n}/%{n}-%{realversion}.tar.gz
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
            --disable-database \
            --enable-termcap

make %{makeprocesses} CFLAGS="-O2 -fPIC" CXXFLAGS="-O2 -fPIC -std=c++11"

%install
make install
