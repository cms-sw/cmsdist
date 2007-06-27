### RPM external mimetic 0.8.9-CMS3
Source: http://codesink.org/download/%{n}-%{realversion}.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%i
make

%install
make install

