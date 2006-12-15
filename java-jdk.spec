### RPM virtual java-jdk 1.0
## INITENV SET JAVA_HOME @JAVA_HOME@
## INITENV +PATH PATH @JAVA_PATH@
## INITENV +PATH LD_LIBRARY_PATH @JAVA_LIB@
Source: none
%prep
%build
%install
%post
if [ -d /afs/cern.ch/sw/java/i386_redhat73/jdk/sun-1.4.2/ ]
then
    JAVA_HOME=/afs/cern.ch/sw/java/i386_redhat73/jdk/sun-1.4.2/
    JAVA_PATH=$JAVA_HOME/bin
    JAVE_LIB=$JAVA_HOME/lib
else
    JAVA_HOME=`echo $(which javac) | sed -e "s|/bin/.*||"`
    JAVA_PATH=$JAVA_HOME/bin
    JAVA_LIB=$JAVA_HOME/lib
fi
perl -p -i -e "s|\@JAVA_HOME\@|$JAVA_HOME|" $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/init.sh
perl -p -i -e "s|\@JAVA_PATH\@|$JAVA_PATH|" $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/init.sh
perl -p -i -e "s|\@JAVA_LIB\@|$JAVA_LIB|" $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/init.sh
perl -p -i -e "s|\@JAVA_HOME\@|$JAVA_HOME|" $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/init.csh
perl -p -i -e "s|\@JAVA_PATH\@|$JAVA_PATH|" $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/init.csh
perl -p -i -e "s|\@JAVA_LIB\@|$JAVA_LIB|" $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/init.csh
