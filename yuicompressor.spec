### RPM external yuicompressor 2.4.7
## INITENV SET YUICOMPRESSOR %i/build/%n-%{realversion}.jar 
## NOCOMPILER

Source: http://yui.zenfs.com/releases/yuicompressor/%n-%{realversion}.zip

%prep
%setup -n %n-%{realversion}

%build

%install
cp -r build %i
