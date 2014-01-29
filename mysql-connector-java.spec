### RPM external mysqlconnectorjava 5.0.5
# Local patches and build system fudging by Lassi A. Tuura <lat@iki.fi>
Requires: mysql java-jdk
%define downloadn mysql-connector-java
Source: http://mirror.switch.ch/ftp/mirror/mysql/Downloads/Connector-J/%{downloadn}-%v.tar.gz

%prep
%setup -q -n %{n}-%v

%build

%install
cp -r * %i
