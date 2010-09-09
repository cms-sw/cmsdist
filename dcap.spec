### RPM external dcap 1.7.0.48
#get dcap from dcache svn repo now...
%define svnTag %(echo %realversion | tr '.' '-')
Source: svn://svn.dcache.org/dCache/tags/production-%svnTag/modules/dcap?scheme=http&module=dcap&output=/dcap.tgz
Patch0: dcap-macosx-workarounds

%define isosx %(case %cmsos in osx*%closingbrace echo true;; *%closingbrace echo false;; esac)
%if "%{?isosx:set}" == "set"
%define soname dylib
%else
%define soname so
%endif

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%if "%cpu" != "amd64"
%define libsuffix %{nil}
%else
%define libsuffix ()(64bit)
%endif

Provides: libdcap.%{soname}%{libsuffix}
Provides: libpdcap.%{soname}%{libsuffix}

%prep
%setup -n dcap
# THIS PATCH IS COMPLETELY UNTESTED AND HAS THE SOLE
# PURPOSE OF BUILDING STUFF ON MAC, REGARDLESS WHETHER
# IT WORKS OR NOT.
case %cmsos in 
 osx*) 
%patch0 -p1
  ;;
esac

%build
chmod +x mkmapfile.sh
chmod +x mkdirs.sh
chmod +x version.sh
LD=gcc make BIN_PATH=%i SONAME=%soname %makeprocesses 
%install
LD=gcc make BIN_PATH=%i SONAME=%soname install
