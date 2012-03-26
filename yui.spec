### RPM external yui 2.8.2r1
## NOCOMPILER

Source: http://yuilibrary.com/downloads/yui2/yui_%realversion.zip 

%prep
%setup -n yui
%build
%install
cp -r build %i
