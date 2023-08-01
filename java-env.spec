### RPM external java-env 1.1
## INITENV SET JAVA_HOME %{java_home}
## INITENV +PATH PATH %{java_home}/bin
## INITENV +PATH LD_LIBRARY_PATH %{java_home}/lib
## NOCOMPILER

%if %{rhel} < 9
# /usr/lib/jvm/java on EL8 contains java 1.8, and Bazel requires java 11
%define java_home /usr/lib/jvm/java-11
%else
%define java_home /usr/lib/jvm/java
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
