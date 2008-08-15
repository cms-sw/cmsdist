### RPM external sherpa 1.1.1
Source: http://www.hepforge.org/archive/sherpa/Sherpa-%realversion.tar.gz

Requires: hepmc lhapdf

Patch: sherpa-lhapdf

%prep
%setup -n SHERPA-MC-%realversion
%patch -p1

%build
# in case of errors the tool prompts ... and the build process hangs forever :(
echo "a" | ./TOOLS/makeinstall -t --copt --enable-hepmc2=$HEPMC_ROOT --copt --enable-lhapdf=$LHAPDF_ROOT --copt --prefix=%i

%install
#make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=z>
<client>
 <Environment name=SHERPA_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$SHERPA_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$SHERPA_BASE/lib"></Environment>
</client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
