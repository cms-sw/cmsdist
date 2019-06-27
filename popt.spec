### RPM external popt 1.16
Source: http://rpm5.org/files/%{n}/%{n}-%{realversion}.tar.gz
%define drop_files %{i}/share

%build
./configure --disable-static --disable-nls \
            --prefix %{i} --build="%{_build}" --host="%{_host}" \
            CFLAGS="-fPIC" \
            CXXFLAGS="-fPIC"  
make
# bla bla
