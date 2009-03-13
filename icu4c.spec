### RPM external icu4c 4_0_1
Source: http://download.icu-project.org/files/icu4c/4.0.1/%n-%realversion-src.tgz

%prep
#%setup -n %n-%{realversion}
%setup -n icu

%build
cd source
chmod +x runConfigureICU configure install-sh
./runConfigureICU Linux --prefix=%i
make

%install
cd source
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=Icu4c version=%v>
<lib name=icu4c>
<client>
 <Environment name=ICU4C_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$ICU4C_BASE/include"></Environment>
 <Environment name=LIBDIR  default="$ICU4C_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$ICU4C_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n

