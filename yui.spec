### RPM external yui 0.12.0
Source: http://puzzle.dl.sourceforge.net/sourceforge/yui/yui_%v.zip 

%prep
%setup -n yui
%build
%install
cp -r * %i
