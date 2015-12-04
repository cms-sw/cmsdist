### RPM external popt-bootstrap 1.16
Source: http://rpm5.org/files/popt/popt-%{realversion}.tar.gz
%define drop_files %{i}/share

%prep  
%setup -n popt-%{realversion}

%build
# Update to get AArch64
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

./configure --disable-static --disable-nls \
            --prefix %{i} --build="%{_build}" --host="%{_host}" \
            CFLAGS="-fPIC" \
            CXXFLAGS="-fPIC"  
make
