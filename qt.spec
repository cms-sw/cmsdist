### RPM external qt 4.8.7
## INITENV UNSET QMAKESPEC
## INITENV SET QTDIR %i

Requires: libjpeg-turbo
Source0: http://download.qt.io/official_releases/qt/4.8/%{realversion}/qt-everywhere-opensource-src-%{realversion}.tar.gz
Patch0: qt-everywhere-opensource-src-4.8.7-gcc6

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
export MAKEFLAGS="%{makeprocesses}"

case %cmsplatf in
  slc*)
    export CONFIG_ARGS="-platform linux-g++"
  ;;
  osx*)
    export CONFIG_ARGS="-no-framework -arch x86_64"
  ;;
esac

# Force system compiler also when using gcc 4.6.1 ++ on mac.  This is required
# because the mainline compiler does not support a bunch of objective-c 2.0
# features which are heavily used in Qt/Cocoa.
case %cmsplatf in
  osx*)
    if [ xcode-select -print-path ]; then
      CMS_XCODE_ROOT="`xcode-select -print-path`"
    fi
    export PATH=$CMS_XCODE_ROOT/usr/bin:$PATH
    export CXX="$CMS_XCODE_ROOT/usr/bin/llvm-g++-4.2"
    export CC="$CMS_XCODE_ROOT/usr/bin/llvm-gcc-4.2"
    export LD="$CMS_XCODE_ROOT/usr/bin/llvm-g++-4.2"
    export LINK="$CMS_XCODE_ROOT/usr/bin/llvm-g++-4.2"
  ;;
esac

rm -rf demos examples doc
echo yes | ./configure -prefix %i -opensource -stl -no-openssl -no-webkit -no-debug \
                       -L$LIBJPEG_TURBO_ROOT/lib64 -no-glib -no-libtiff -no-libpng -no-libmng \
                       -no-dwarf2 -no-phonon -no-multimedia -no-stl -no-exceptions \
                       -no-separate-debug-info -no-multimedia -no-sql-sqlite -no-sql-odbc \
                       -no-javascript-jit -no-script -no-scripttools -no-avx -no-rpath \
                       -no-sql-psql -no-sql-mysql $CONFIG_ARGS \
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
# bla bla
