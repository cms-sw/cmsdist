### RPM external dablooms 0.9.1

Source: https://github.com/bitly/dablooms/archive/v%realversion.tar.gz

%prep
%setup -n dablooms-%realversion

%build
make all

%install
make install prefix=%i
