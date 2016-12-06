### RPM external gosam 2.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib
## INITENV +PATH DYLD_LIBRARY_PATH %{i}/lib

# Download from official webpage
Source: https://gosam.hepforge.org/gosam-contrib-%{realversion}-latest.tar.gz


%define keep_archives true

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif


%prep
%setup -q -n gosam-contrib-%{realversion}


%build
CXX="$(which %{cms_cxx}) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"


./configure $PLATF_CONF_OPTS \
            --prefix=%{i} \
            CXX="$CXX" CC="$CC"  



make %{makeprocesses}

%install
make install
find %{i}/lib -name '*.la' -exec rm -f {} \;

%post
