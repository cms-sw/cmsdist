### RPM external java-env 11.0
## INITENV SET JAVA_HOME %{java_home}
## INITENV +PATH PATH %{java_home}/bin
## INITENV +PATH LD_LIBRARY_PATH %{java_home}/lib
## NOCOMPILER

%define java_home /usr/lib/jvm/java
%if 0%{?rhel:1}
%if 0%{?rhel} < 9
# /usr/lib/jvm/java on EL8 contains java 1.8, and Bazel requires java 11
%define java_home /usr/lib/jvm/java-11
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
