### RPM external java-env 11_17
## INITENV SET JAVA_HOME %{java_home}
## INITENV +PATH PATH %{java_home}/bin
## INITENV +PATH LD_LIBRARY_PATH %{java_home}/lib
## NOCOMPILER

#For RHEL: Use java 11 for el7 and java 17 for el8 and above
#Nor non RHEL e.g FC: use default system java
%define java_home /usr/lib/jvm/java
%if 0%{?rhel:1}
%if %{?rhel} < 8
%define java_home /usr/lib/jvm/java-11
%endif
%if %{?rhel} > 7
%define java_home /usr/lib/jvm/java-17
%endif
%endif
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
