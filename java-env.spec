### RPM external java-env 1.1
## INITENV SET JAVA_HOME %{java_home}
## INITENV +PATH PATH %{java_home}/bin
## INITENV +PATH LD_LIBRARY_PATH %{java_home}/lib
## NOCOMPILER

%define java_home /usr/lib/jvm/java
Source: none

%prep

%build

%install

if [ ! -e %{java_home}/bin/javac ] ; then
  echo "%{java_home}/bin/javac path is not available"
  exit 1
fi
%{java_home}/bin/javac -version
%{java_home}/bin/java -version
# bla bla
