### RPM external jimmy 4.2
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac 

Requires: herwig
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch: jimmy-4.2-gfortran

%prep
%setup -q -n %{n}/%{realversion}
case %gccver in
  4.*)
%patch -p0
  ;;
esac

%build
./configure --with-herwig=$HERWIG_ROOT
make 

%install
tar -c lib include | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="jimmy" version="%v">
    <lib name="jimmy"/>
    <client>
      <environment name="JIMMY_BASE" default="%i"/>
      <environment name="LIBDIR" default="$JIMMY_BASE/lib"/>
      <environment name="INCLUDE" default="$JIMMY_BASE/include"/>
    </client>
    <use name="f77compiler"/>
    <use name="herwig"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
