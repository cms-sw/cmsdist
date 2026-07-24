### RPM external java-env 17_21
## INITENV SET JAVA_HOME %{java_home}
## INITENV +PATH PATH %{java_home}/bin
## INITENV +PATH LD_LIBRARY_PATH %{java_home}/lib
## NOCOMPILER
%define skip_license_checks 1
#For RHEL: Use java 21
#Nor non RHEL e.g FC: use default system java
%define java_home /usr/lib/jvm/java-21
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
