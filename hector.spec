### RPM external hector 1_3_4
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac 

%define rname Hector
%define realversion %(echo %v | cut -d- -f1 )
Requires: root
Source: http://www.fynu.ucl.ac.be/themes/he/ggamma/hector/%{rname}_%{realversion}.tbz

%prep
%setup -q -n %{rname}_%{realversion}

%build
perl -p -i -e "s|^ROOTLIBS.*$|ROOTLIBS=-L$ROOT_ROOT/lib -lCore -lRint -lMatrix -lPhysics -lCint -lMathCore -pthread -lm -ldl -rdynamic|" Makefile
make

%install
tar -c . | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="Hector" version="%v">
    <info url="http://www.fynu.ucl.ac.be/themes/he/ggamma/hector/"/>
    <lib name="Hector"/>
    <client>
      <environment name="HECTOR_BASE" default="%i"/>
      <environment name="LIBDIR" default="$HECTOR_BASE/lib"/>
      <environment name="INCLUDE" default="$HECTOR_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
