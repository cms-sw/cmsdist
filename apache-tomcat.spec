### RPM external apache-tomcat 5.5.20
Source: http://download.nextag.com/apache/tomcat/tomcat-5/v5.5.20/bin/apache-tomcat-5.5.20.tar.gz
Requires: java-jdk
%build
cd bin
tar xfz jsvc.tar.gz
cd jsvc-src
chmod +x configure
./configure
make
%install
cp -r ./* %i

