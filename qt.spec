### RPM external qt 4.8.1
## INITENV UNSET QMAKESPEC
## INITENV SET QTDIR %i

Requires: libjpg 
Source0: ftp://ftp.qt.nokia.com/qt/source/%n-everywhere-opensource-src-%{realversion}.tar.gz
Patch0: qt-4.8.0-fix-gcc47

%define strip_files %i/lib %i/bin

%prep
%setup -T -b 0 -n %n-everywhere-opensource-src-%{realversion}
%patch0 -p1

%build
unset QMAKESPEC || true
export QTDIR=$PWD
export PATH=$QTDIR/bin:$PATH
export LD_LIBRARY_PATH=$QTDIR/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$QTDIR/lib:$DYLD_LIBRARY_PATH

case %cmsplatf in
  slc*)
    export CONFIG_ARGS="-platform linux-g++-64"
  ;;
  osx*)
    export CONFIG_ARGS="-no-framework -arch x86_64"
  ;;
esac

# Force system compiler also when using gcc 4.6.1 ++ on mac.  This is required
# because the mainline compiler does not support a bunch of objective-c 2.0
# features which are heavily used in Qt/Cocoa.
case %cmsplatf in
  osx*_*_gcc421) ;;
  osx*)
    if [ xcode-select -print-path ]; then
      CMS_XCODE_ROOT="`xcode-select -print-path`"
    fi
    export PATH=$CMS_XCODE_ROOT/usr/bin:$PATH
    export CXX="/usr/bin/llvm-g++"
    export CC="/usr/bin/llvm-gcc"
    export LD="/usr/bin/llvm-g++"
    export LINK="/usr/bin/llvm-g++"
  ;;
esac

rm -rf demos examples doc
echo yes | ./configure -prefix %i -opensource -stl -no-openssl -no-webkit -no-debug \
                       -L$LIBJPG_ROOT/lib -no-glib -no-libtiff -no-libpng -no-libmng \
                       -no-dwarf2 -no-phonon -no-multimedia -no-stl -no-exceptions \
                       -no-separate-debug-info -no-multimedia -no-sql-sqlite -no-sql-odbc -no-sql-mysql $CONFIG_ARGS \
                       -make "libs tools"

make %makeprocesses

%install
make install
# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config 
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig
rm -rf %i/lib/*.la

# Qt itself has some paths that can only be overwritten by
# using an appropriate `qt.conf`.
# Without this qmake will complain whenever used in
# a directory different than the build one.
mkdir -p %i/bin
cat << \EOF_QT_CONF >%i/bin/qt.conf
[Paths]
Prefix = %{i}
EOF_QT_CONF

%post
%{relocateConfig}bin/qt.conf
%{relocateConfig}mkspecs/qconfig.pri
