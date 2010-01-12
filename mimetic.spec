### RPM external mimetic 0.9.6
Source: http://codesink.org/download/%{n}-%{realversion}.tar.gz
Patch0: mimetic-0.9.5-amd64-uint
Patch1: mimetic-0.9.6-uint32_t-gcc44

%prep
%setup -n %n-%{realversion}

case %cmsplatf in
*gcc4* | osx*)
%patch0 -p1
esac

case %gccver in
  4.4.*)
%patch1 -p1
  ;;
esac

%build
./configure --prefix=%i
make

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="mimetic" version="%v">
    <lib name="mimetic"/>
    <client>
      <environment name="MIMETIC_BASE" default="%i"/>
      <environment name="LIBDIR" default="$MIMETIC_BASE/lib"/>
      <environment name="INCLUDE" default="$MIMETIC_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
