### RPM external java-env 1.0
## INITENV SET JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.131-2.b11.el7_3.x86_64

Source: none

%prep

%build



%install

echo $JAVA_HOME
if [ ! -d "$JAVA_HOME" ]; then
  echo "JAVA_HOME path is not available"
  echo "$JAVA_HOME"
  exit 1
fi



