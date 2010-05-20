### RPM external extjs 3.1.1
Source: http://extjs.cachefly.net/ext-%realversion.zip

%prep
unzip %{_sourcedir}/ext-%realversion.zip
%build
%install
cp -rp ext-%realversion/* %i
