### RPM external extjs 3.1.1
Source: http://extjs.cachefly.net/ext-%realversion.zip

%prep
%setup -n ext-%realversion
%build
%install
cp -rp * %i
rm -fr %i/{docs,examples}
