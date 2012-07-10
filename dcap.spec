### RPM external dcap 2.47.5.0
#get dcap from dcache svn repo now...
Source: http://cmsrep.cern.ch/cmssw/download/dcap/dcap.tgz
#Source: svn://svn.dcache.org/dCache/tags/dcap-2.47.5-0?scheme=http&module=dcap&output=/dcap.tgz
Patch0: dcap-2.47.5.0-macosx
Patch1: dcap-2.47.5.0-fork-safety

# Unfortunately I could not find any rpm version invariant way to do and "if
# else if", so I ended up hardcoding all the possible variants.
# FIXME: move to multiple ifs once rpm 4.4.2.2 is deprecated.
Provides: libdcap.so
Provides: libpdcap.so
Provides: libdcap.so()(64bit)
Provides: libpdcap.so()(64bit)
Provides: libdcap.dylib
Provides: libpdcap.dylib

BuildRequires: autotools

%prep
%setup -n dcap
# THIS PATCH IS COMPLETELY UNTESTED AND HAS THE SOLE PURPOSE OF BUILDING STUFF
# ON MAC, REGARDLESS WHETHER IT WORKS OR NOT. It is however safe to include,
# since every change is ifdeffed with __APPLE__.
%patch0 -p1
# Apply fork safety patch from Brian Bockelman
%patch1 -p0

%build
# Since we are using the checked out code, we need to regenerate the auto-tools
# crap.
mkdir -p config
aclocal -I config
autoheader
libtoolize --automake
automake --add-missing --copy --foreign
autoconf
./configure --prefix %i

# We don't care about the plugins and other stuff and build only the source.
make -C src %makeprocesses
%install
make -C src install

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
# Look up documentation online.
%define drop_files %i/share