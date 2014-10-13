### RPM external eigen 3.2.2
## NOCOMPILER
Source: http://bitbucket.org/%{n}/%{n}/get/%{realversion}.tar.gz
   
%prep
%setup -n %n-%n-1306d75b4a21

%build
mkdir -p %i/include

%install
cp -r Eigen %i/include

