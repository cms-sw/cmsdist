### RPM external apache-tomcat 5.5.26
Source: http://download.nextag.com/apache/tomcat/tomcat-5/v5.5.26/bin/apache-tomcat-5.5.26.tar.gz
Requires: java-jdk
%build
source $JAVA_JDK_ROOT/etc/profile.d/init.sh
export JAVA_HOME=$JAVA_JDK_ROOT 
cd bin
tar xfz jsvc.tar.gz
cd jsvc-src
chmod +x configure
./configure
make
%install
cp -r ./* %i

%post
# setup environment
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
cat $APACHE_TOMCAT_ROOT/conf/server.xml | \
sed 's,connectionTimeout="20000" disableUploadTimeout="true",connectionTimeout="20000" disableUploadTimeout="true" maxPostSize="0",g' > $APACHE_TOMCAT_ROOT/conf/server.xml.tmp
mv $APACHE_TOMCAT_ROOT/conf/server.xml.tmp $APACHE_TOMCAT_ROOT/conf/server.xml
#
# bla bla
