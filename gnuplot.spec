### RPM external gnuplot 4.6.1
Source: http://downloads.sourceforge.net/project/gnuplot/gnuplot/4.6.1/gnuplot-4.6.1.tar.gz

%prep
%setup -n %n-%realversion

%build
./configure --prefix %i --disable-wxt --without-cairo --without-tutorial --without-x
make %makeprocesses

%install
make install
