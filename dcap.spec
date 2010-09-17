### RPM external dcap 1.7.0.48
#get dcap from dcache svn repo now...
%define svnTag %(echo %realversion | tr '.' '-')
Source: svn://svn.dcache.org/dCache/tags/production-%svnTag/modules/dcap?scheme=http&module=dcap&output=/dcap.tgz
Patch0: dcap-macosx-workarounds

%define isosx %(case %cmsos in osx*%closingbrace echo true;; *%closingbrace echo false;; esac)
%define cpu %(echo %cmsplatf | cut -d_ -f2)

# Determine the soname and the suffix for the libraries.
# We do it this way because rpm does not support nested
# ifs.
%if "%{?isosx:set}-%{cpu}" == "set-amd64"
%define soname dylib
%define libsuffix %{nil}
%endif

%if "%{?isosx:set}-%{cpu}" == "set-ia32"
%define soname dylib
%define libsuffix %{nil}
%endif

%if "%{?isosx:set}-${cpu}" == "-amd64"
%define soname so 
%define libsuffix ()(64bit)
%endif

%if "%{?isosx:set}-${cpu}" == "-ia32"
%define soname so
%define libsuffix %{nil} 
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
