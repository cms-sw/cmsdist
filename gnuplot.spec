### RPM external gnuplot 5.2.8
Source: http://downloads.sourceforge.net/project/gnuplot/gnuplot/%{realversion}/gnuplot-%{realversion}.tar.gz
Requires: zlib

%prep
%setup -n %{n}-%{realversion}

%build
CFLAGS=-I${ZLIB_ROOT}/include \
LDFLAGS=-L${ZLIB_ROOT}/lib \
./configure \
  --prefix %{i} \
  --disable-wxt \
  --without-cairo \
  --without-tutorial \
  --without-readline \
  --without-gd \
  --without-x \
  --without-lua

make %{makeprocesses}

%install
make install
