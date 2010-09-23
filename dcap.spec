### RPM external dcap 1.7.0.48
#get dcap from dcache svn repo now...
%define svnTag %(echo %realversion | tr '.' '-')
Source: svn://svn.dcache.org/dCache/tags/production-%svnTag/modules/dcap?scheme=http&module=dcap&output=/dcap.tgz
Patch0: dcap-macosx-workarounds

# Unfortunately I could not find any rpm version invariant way to do and "if
# else if", so I ended up hardcoding all the possible variants.
# FIXME: move to multiple ifs once rpm 4.4.2.2 is deprecated.
Provides: libdcap.so
Provides: libpdcap.so
Provides: libdcap.so()(64bit)
Provides: libpdcap.so()(64bit)
Provides: libdcap.dylib
Provides: libpdcap.dylib

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
case %cmsos in
  osx*)
	SONAME=dylib ;;
  slc*)
	SONAME=so ;;
esac	

LD=gcc make BIN_PATH=%i SONAME=$SONAME %makeprocesses
%install
case %cmsos in
  osx*)
        SONAME=dylib ;;
  slc*)
        SONAME=so ;;
esac    
LD=gcc make BIN_PATH=%i SONAME=$SONAME install
