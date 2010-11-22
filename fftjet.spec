### RPM external fftjet 1.3.1
Source: http://www.hepforge.org/archive/fftjet/%n-%realversion.tar.gz
Requires: fftw3

%prep
%setup -n %n-%realversion

%build
./configure --enable-shared --disable-dependency-tracking --enable-threads --prefix=%i
make %makeprocesses

%install
make install
