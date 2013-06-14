### RPM virtual xsl-virtual 1.0.33
Source: none
Provides: libexslt.so.0  
Provides: libxslt.so.1  
Provides: libxsltbreakpoint.so.1  
Provides: libxslt 
%prep
%build
%install
echo 'This is only a virtual package, please install your distribution libxslt.rpm or equivalent'> %{i}/README 
