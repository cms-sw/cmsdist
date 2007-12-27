### RPM external dcap 1.2.35-CMS19
# Fakes the presence of dcap since we are not allowed to distribute it.
Source: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%n-%realversion.tar.gz
Patch: http://service-spi.web.cern.ch/service-spi/external/tarFiles/%n-%realversion.patch
%define cpu %(echo %cmsplatf | cut -d_ -f2)
%if "%cpu" != "amd64"
%define libsuffix %{nil}
%else
%define libsuffix ()(64bit)
%endif

Provides: libdcap.so%{libsuffix}
Provides: libpdcap.so%{libsuffix}
%prep
rm -rf %n-%realversion
%setup -n %n-%realversion
%patch0 -p1
%build
rm -rf %i
mkdir -p %i
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
