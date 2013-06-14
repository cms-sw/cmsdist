### RPM external apr 1.2.6
Source: http://mirror1.zic-network.ch/apache/%{n}/%{n}-%{v}.tar.gz
%build
./configure --prefix=%{i}
make %makeprocesses
