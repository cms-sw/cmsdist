### RPM external popt-bootstrap 1.16
Source: http://rpm5.org/files/popt/popt-%{realversion}.tar.gz
%define drop_files %{i}/share

%build
./configure --disable-static --disable-nls \
            --prefix %{i} --build="%{_build}" --host="%{_host}" \
            CFLAGS="-fPIC" \
            CXXFLAGS="-fPIC"  
make
