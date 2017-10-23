### RPM external gosamcontrib 2.0-20150803
Source: http://www.hepforge.org/archive/gosam/gosam-contrib-%{realversion}.tar.gz

Requires: qgraf
Requires: form

%prep
%setup -q -n gosam-contrib-2.0

%build
CXX="$(which c++) -fPIC"
CC="$(which gcc) -fPIC"
FC="$(which gfortran)"
PLATF_CONF_OPTS="--enable-shared --enable-static"

./configure $PLATF_CONF_OPTS \
            --prefix=%i \
            --bindir=%i/bin \
            --libdir=%i/lib \
            CXX="$CXX" CC="$CC" FC="$FC" 

make %makeprocesses all

%install
make install 

%post
%{relocateConfig}share/gosam-contrib/gosam.conf

