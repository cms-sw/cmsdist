### RPM external atlas 3.10.3
#Source: https://sourceforge.net/projects/math-atlas/files/Stable/%realversion/atlas%realversion.tar.bz2
#Source: https://downloads.sourceforge.net/project/math-atlas/Stable/%realversion/atlas%realversion.tar.bz2
Source: https://sourceforge.net/projects/math-atlas/files/Stable/%realversion/atlas%realversion.tar.bz2/download
Requires: lapack

#BuildRequires: cmake

%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n ATLAS

%build
mkdir buildDir
cd buildDir
../configure -b 64 -D c -DPentiumCPS=2400 --prefix=%i --shared
export LAPACK_ROOT
export LAPACK=$LAPACK_ROOT/lib/liblapack.$SONAME
LDFLAGS="$LDFLAGS $LAPACK" \
make %{makeprocesses} build
#make check
#make ptcheck
#make time
cd -

%install
cd buildDir
make install
cd -
# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config 
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig
