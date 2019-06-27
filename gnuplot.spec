### RPM external gnuplot 4.6.5
Source: http://downloads.sourceforge.net/project/gnuplot/gnuplot/%{realversion}/gnuplot-%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build
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
# bla bla
