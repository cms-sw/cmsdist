### RPM external mpfr 2.2.1
Source: http://www.mpfr.org/mpfr-current/%n-%v.tar.gz

%prep
%setup -n %n-%v

%build
./configure --prefix=%i
gmake

%install
gmake install
