### RPM external protobuf 2.4.1
Source: http://protobuf.googlecode.com/files/protobuf-%realversion.tar.bz2
Requires: zlib

%prep
%setup -n protobuf-%realversion

%build
./configure --prefix %{i} \
    CXXFLAGS="-I$ZLIB_ROOT/include" \
    CFLAGS="-I$ZLIB_ROOT/include" \
    LDFLAGS="-L$ZLIB_ROOT/lib"
make %{makeprocesses}

%install
make install
