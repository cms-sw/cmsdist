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

