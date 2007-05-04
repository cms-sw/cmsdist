
### RPM external  apt 0.5.15cnc6
#Requires: beecrypt-devel
Source: http://www.uscms.org/SoftwareComputing/CMSSoftware/download/apt_%v.tar.gz

%prep
%setup -q -n %v

./configure --prefix=%{i} --exec-prefix=%{i} --disable-nls --disable-dependency-tracking 

%build
make 

%install
make install
