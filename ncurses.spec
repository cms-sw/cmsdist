### RPM external ncurses 5.9
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://ftp.gnu.org/pub/gnu/%{n}/%{n}-%{realversion}.tar.gz
%define keep_archives true
%define drop_files %{i}/lib/*.so

%prep
%setup -n %{n}-%{realversion}

%build
%if "%mic" == "true"
 CXX="icpc -fPIC -mmic" CC="icc -fPIC -mmic" \
./configure --prefix="%{i}" \
            --build="%{_build}" \
            --host="x86_64-k1om-linux" \
            --disable-shared \
            --enable-static \
            --without-debug \
            --without-ada \
            --without-manpages \
            --disable-database \
            --enable-termcap
%else
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
%endif
make %{makeprocesses} CFLAGS="-O2 -fPIC" CXXFLAGS="-O2 -fPIC -std=c++11"

%install
make install
