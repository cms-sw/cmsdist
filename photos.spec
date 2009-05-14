### RPM external photos 215.5
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}/%{realversion}

%build
./configure --lcgplatform=%cmsplatf
make 

%install
tar -c lib include | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=photos version=%v>
<Client>
 <Environment name=PHOTOS_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$PHOTOS_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$PHOTOS_BASE/include"></Environment>
</Client>
<lib name=photos>
<use name=f77compiler>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
