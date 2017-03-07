### RPM external form 4.1.033e
Source: https://gosam.hepforge.org/gosam-installer/form-%{realversion}.tar.gz





%prep
%setup -q -n form-4.1


%build



CXX="$(which g++) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"

./configure $PLATF_CONF_OPTS \
            --prefix=%i \
            --bindir=%i/bin \
            --without-gmp \
            CXX="$CXX" CC="$CC" CXXFLAGS=-fpermissive

make %makeprocesses

%install
make install 


