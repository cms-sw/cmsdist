### RPM external toprex 4.23-CMS8
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch: toprex-4.23-gfortran

%prep
%setup -q -n %{n}/%{realversion}
%if "%cmsplatf" == "slc4_ia32_gcc412"
%patch -p0 
%endif
./configure --lcgplatform=%cmsplatf

%build
make 

%install
tar -c lib include | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=toprex version=%v>
<Client>
 <Environment name=TOPREX_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$TOPREX_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$TOPREX_BASE/include"></Environment>
</Client>
<lib name=toprex>
<use name=f77compiler>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
