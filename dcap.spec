### RPM external dcap 1.7.0.48
#get dcap from dcache svn repo now...
%define svnTag %(echo %realversion | tr '.' '-')
Source: svn://svn.dcache.org/dCache/tags/production-%svnTag/modules/dcap?scheme=http&module=dcap&output=/dcap.tgz

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%if "%cpu" != "amd64"
%define libsuffix %{nil}
%else
%define libsuffix ()(64bit)
%endif

Provides: libdcap.so%{libsuffix}
Provides: libpdcap.so%{libsuffix}
%prep
%setup -n dcap

%build
chmod +x mkmapfile.sh
chmod +x mkdirs.sh
chmod +x version.sh
LD=gcc make BIN_PATH=%i %makeprocesses 
%install
LD=gcc make BIN_PATH=%i install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=dcap>
<Client>
 <Environment name=DCAP_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$DCAP_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$DCAP_BASE/include"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
