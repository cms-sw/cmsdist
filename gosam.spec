### RPM external gosam 2.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib
## INITENV +PATH DYLD_LIBRARY_PATH %{i}/lib

# Download from official webpage
Source: https://gosam.hepforge.org/gosam-contrib-%{realversion}-latest.tar.gz

Requires: python

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


# Update to detect aarch64 and ppc64le
rm -f ./Config/config.{sub,guess}
curl -L -k -s -o ./Config/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./Config/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./Config/config.{sub,guess}

./configure $PLATF_CONF_OPTS \
            --prefix=%{i} \
            CXX="$CXX" CC="$CC"  



make %{makeprocesses}

%install
make install
find %{i}/lib -name '*.la' -exec rm -f {} \;

%post
