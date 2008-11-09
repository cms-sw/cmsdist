### RPM external jimmy 4.2
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
./configure --with-herwig=$HERWIG_ROOT

%build
make 

%install
tar -c lib include | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n

<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=jimmy version=%v>
<lib name=jimmy>
<Client>
 <Environment name=JIMMY_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$JIMMY_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$JIMMY_BASE/include"></Environment>
</Client>
<use name=f77compiler>
<use name=herwig>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
