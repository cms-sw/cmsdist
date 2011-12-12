### RPM external yui3 3.4.1
## NOCOMPILER

Source: http://yui.zenfs.com/releases/yui3/yui_%realversion.zip

%prep
%setup -n yui

%build

%install
cp -r build %i
