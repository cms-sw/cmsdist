### RPM external dcap 1.7.0.31
#get dcap from dcache now...
Source: http://www.dcache.org/downloads/1.7.0/dCache-production-1-7-0-31.tar.gz

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%if "%cpu" != "amd64"
%define libsuffix %{nil}
%else
%define libsuffix ()(64bit)
%endif

Provides: libdcap.so%{libsuffix}
Provides: libpdcap.so%{libsuffix}
%prep
#rm -rf %n-%realversion
%setup -n dCacheBuild

%build
cd modules/dcap
chmod +x mkmapfile.sh
chmod +x mkdirs.sh
chmod +x version.sh
LD=gcc make BIN_PATH=%i %makeprocesses 
%install
cd modules/dcap
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
