### RPM external extjs 3.1.1
Source: http://extjs.cachefly.net/%n-%realversion.zip

%prep
unzip %{_sourcedir}/%n-%realversion.zip
%build
%install
cp -rp %n-%realversion/* %i
