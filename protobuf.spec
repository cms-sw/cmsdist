### RPM external protobuf 2.6.1
Source: https://github.com/google/protobuf/releases/download/v%{realversion}/protobuf-%{realversion}.tar.gz
Requires: zlib

%prep
%setup -n protobuf-%realversion

%build
./configure --prefix %{i} --disable-static \
    CXXFLAGS="-I$ZLIB_ROOT/include" \
    CFLAGS="-I$ZLIB_ROOT/include" \
    LDFLAGS="-L$ZLIB_ROOT/lib"
make %{makeprocesses}

%install
make install
rm -rf %i/lib/pkgconfig
