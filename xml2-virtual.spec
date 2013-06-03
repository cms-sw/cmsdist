### RPM virtual xml2-virtual 2.5.10
Source: none
Provides: libxml2.so.2  
Provides: libxml2 
%prep
%build
%install
echo 'This is only a virtual package, please install your distribution libxml2.rpm or equivalent'> %{i}/README 
