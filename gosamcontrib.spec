### RPM external gosamcontrib 2.0-20200904
Source: https://github.com/gudrunhe/gosam-contrib/archive/gosam-contrib-%{realversion}.tar.gz

Requires: qgraf
Requires: form
BuildRequires: autotools

%prep
%setup -q -n gosam-contrib-gosam-contrib-%{realversion}

%build
CXX="$(which c++) -fPIC"
CC="$(which gcc) -fPIC"
FC="$(which gfortran) -std=legacy"
PLATF_CONF_OPTS="--enable-shared --enable-static"

./autogen.sh $PLATF_CONF_OPTS \
            --prefix=%i \
            --bindir=%i/bin \
            --libdir=%i/lib \
            CXX="$CXX" CC="$CC" FC="$FC" F77="${FC}"

make %makeprocesses all

%install
make install 

%post
%{relocateConfig}share/gosam-contrib/gosam.conf

