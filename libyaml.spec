### RPM external libyaml 0.1.3
Source: http://pyyaml.org/download/libyaml/yaml-%realversion.tar.gz

%prep
%setup -n yaml-%realversion

%build
./configure --prefix=%i
make %makeprocesses

%install
make install
