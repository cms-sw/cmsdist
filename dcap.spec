### RPM external dcap 2.47.5.0
#get dcap from dcache svn repo now...
Source: svn://svn.dcache.org/dCache/tags/dcap-2.47.5-0?scheme=http&module=dcap&output=/dcap.tgz
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
sh bootstrap.sh
./configure --prefix %i
make -C src %makeprocesses
%install
make -C src install
