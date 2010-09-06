### RPM external qt 4.6.3
## INITENV UNSET QMAKESPEC
## INITENV SET QTDIR %i

Requires: libjpg 
Source0: ftp://ftp.qt.nokia.com/qt/source/%n-everywhere-opensource-src-%{realversion}.tar.gz

%prep
%setup -T -b 0 -n %n-everywhere-opensource-src-%{realversion}

%build
unset QMAKESPEC || true
export QTDIR=$PWD
export PATH=$QTDIR/bin:$PATH
export LD_LIBRARY_PATH=$QTDIR/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$QTDIR/lib:$DYLD_LIBRARY_PATH

case %cmsplatf in
  slc*_amd64*)
    export CONFIG_ARGS="-platform linux-g++-64"
  ;;
  osx*_ia32*)
    export CONFIG_ARGS="-no-framework"
  ;;
  osx*_amd64*)
    export CONFIG_ARGS="-no-framework -arch x86_64"
  ;;
esac

rm -rf demos examples doc
echo yes | ./configure -prefix %i -opensource -stl -no-openssl -L$LIBJPG_ROOT/lib -no-glib -no-libtiff -no-libpng -no-libmng -no-separate-debug-info -no-sql-odbc -no-sql-mysql $CONFIG_ARGS -make "libs tools"

# The following is a kludge around the fact that the fact that the 
# /usr/lib/libfontconfig.so soft link (for 32-bit lib) is missing
# on the 64-bit machines
case %cmsplatf in
  slc*_ia32*)
    mkdir -p %{_builddir}/lib
    ln -s /usr/lib/libfontconfig.so.1 %{_builddir}/%n-all-opensource-src-%{realversion}/lib/libfontconfig.so
    ;;
esac

make %makeprocesses

%install
make install

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
%{relocateConfig}lib/libQt3Support.la     
%{relocateConfig}lib/libQtSql.la
%{relocateConfig}lib/libQtCLucene.la      
%{relocateConfig}lib/libQtSvg.la
%{relocateConfig}lib/libQtCore.la     
%{relocateConfig}lib/libQtTest.la
%{relocateConfig}lib/libQtGui.la      
%{relocateConfig}lib/libQtWebKit.la
%{relocateConfig}lib/libQtHelp.la     
%{relocateConfig}lib/libQtXml.la
%{relocateConfig}lib/libQtNetwork.la      
%{relocateConfig}lib/libQtXmlPatterns.la
%{relocateConfig}lib/libQtOpenGL.la     
%{relocateConfig}lib/libQtScript.la     
%{relocateConfig}bin/qt.conf
%{relocateConfig}mkspecs/qconfig.pri
