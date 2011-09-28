### RPM external libyaml 0.1.3
Source: http://pyyaml.org/download/libyaml/yaml-%realversion.tar.gz

%prep
%setup -n yaml-%realversion

%build
./configure --prefix=%i
make %makeprocesses

%install
make install

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
