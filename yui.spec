### RPM external yui 2.9.0
## NOCOMPILER

Source: http://yuilibrary.com/downloads/yui2/yui_%realversion.zip 

%prep
%setup -n yui
%build
%install
cp -r build %i
