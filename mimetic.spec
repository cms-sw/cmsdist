### RPM external mimetic 0.8.9-CMS3
Source: http://codesink.org/download/%{n}-%{realversion}.tar.gz
Patch0: mimetic-0.8.9-gcc412

%prep
%setup -n %n-%{realversion}
%patch0 -p1

%build
./configure --prefix=%i
make

%install
make install

