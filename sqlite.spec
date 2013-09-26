### RPM external sqlite 3.7.17
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://www.sqlite.org/2013/sqlite-autoconf-3071700.tar.gz

%prep
%setup -n sqlite-autoconf-3071700

%build
case %{cmsplatf} in
   *_mic_* )
    CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" \
    ./configure --build="%{_build}" --host="x86_64-k1om-linux" --prefix=%{i} \
            --disable-tcl --disable-static
     ;;
   * )
    ./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-tcl --disable-static
     ;;
esac
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
