### RPM external polymaps 2.5.1
## NOCOMPILER

Source: https://github.com/simplegeo/%n/zipball/v%{realversion}

%prep
%setup -n simplegeo-%n-2265203

%build

%install
mkdir -p %i/data
cp LICENSE *.js %i/data
find %i/data -type f -exec chmod 644 {} \;
