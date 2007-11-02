### RPM external photos 215-CMS18
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}/%{realversion}
./configure --lcgplatform=%cmsplatf

%build
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
