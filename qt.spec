### RPM external qt 4.5.2
## INITENV UNSET QMAKESPEC
## INITENV SET QTDIR %i

Requires: libjpg 
Source0: ftp://ftp.trolltech.com/qt/source/%n-all-opensource-src-%{realversion}.tar.bz2

%prep
%setup -T -b 0 -n %n-all-opensource-src-%{realversion}

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
  osx*)
    export CONFIG_ARGS="-no-framework"
  ;;
esac

echo yes | ./configure -prefix %i -opensource -stl -no-openssl -L$LIBJPG_ROOT/lib -no-glib -no-libtiff -no-libpng -no-libmng -no-separate-debug-info -no-sql-odbc -no-sql-mysql $CONFIG_ARGS

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

# Remove the doc, as it is large and we don't need that in
# our rpms (it is all available on the web in any case)
rm -fR %i/doc
# Remove also the demos and examples as they are not generally
# useful from our rpm's and SW area
rm -fR %i/demos
rm -fR %i/examples

# Qt itself has some paths that can only be overwritten by
# using an appropriate `qt.conf`.
# Without this qmake will complain whenever used in
# a directory different than the build one.
mkdir -p %i/bin
cat << \EOF_QT_CONF >%i/bin/qt.conf
[Paths]
Prefix = %{i}
EOF_QT_CONF

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/qtbase.xml
  <tool name="qtbase" version="%v">
    <info url="http://www.trolltech.com/products/qt.html"/>
    <lib name="QtCore"/>
    <lib name="QtXml"/>
    <client>
      <environment name="QTBASE_BASE" default="%i"/>
      <environment name="LIBDIR" default="$QTBASE_BASE/lib"/>
      <environment name="INCLUDE" default="$QTBASE_BASE/include"/>
      <environment name="INCLUDE" default="$QTBASE_BASE/include/Qt"/>
      <environment name="INCLUDE" default="$QTBASE_BASE/include/QtCore"/>
      <environment name="INCLUDE" default="$QTBASE_BASE/include/QtXml"/>
    </client>
    <flags cppdefines="QT_ALTERNATE_QTSMANIP QT_CLEAN_NAMESPACE QT_THREAD_SUPPORT"/>
    <runtime name="PATH" value="$QTBASE_BASE/bin" type="path"/>
    <use name="zlib"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qt3support.xml
  <tool name="qt3support" version="%v">
    <info url="http://www.trolltech.com/products/qt.html"/>
    <lib name="Qt3Support"/>
    <client>
      <environment name="QT3SUPPORT_BASE" default="%i"/>
      <environment name="INCLUDE" default="$QT3SUPPORT_BASE/include/Qt3Support"/>
    </client>
    <flags cppdefines="QT3_SUPPORT"/>
    <use name="qtbase"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qt.xml
  <tool name="qt" version="%v">
    <info url="http://www.trolltech.com/products/qt.html"/>
    <lib name="QtOpenGL"/>
    <lib name="QtGui"/>
    <client>
      <environment name="QT_BASE" default="%i"/>
      <environment name="INCLUDE" default="$QT_BASE/include/QtOpenGL"/>
      <environment name="INCLUDE" default="$QT_BASE/include/QtGui"/>
    </client>
    <use name="qtbase"/>
    <use name="qt3support"/>
    <use name="X11"/>
    <use name="opengl"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qtdesigner.xml
  <tool name="qtdesigner" version="%v">
    <info url="http://www.trolltech.com/products/qt.html"/>
    <lib name="QtDesigner"/>
    <client>
      <environment name="QTDESIGNER_BASE" default="%i"/>
      <environment name="INCLUDE" default="$QTDESIGNER_BASE/include/QtDesigner"/>
    </client>
    <use name="qtbase"/>
    <use name="qt"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qtextra.xml
  <tool name="qtextra" version="%v">
    <info url="http://www.trolltech.com/products/qt.html"/>
    <lib name="QtScript"/>
    <client>
      <environment name="QTEXTRA_BASE" default="%i"/>
      <environment name="INCLUDE" default="$QTEXTRA_BASE/include/QtScript"/>
    </client>
    <use name="qtbase"/>
  </tool>
EOF_TOOLFILE

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
%{relocateConfig}etc/scram.d/qtbase.xml
%{relocateConfig}etc/scram.d/qt.xml
%{relocateConfig}etc/scram.d/qtdesigner.xml
%{relocateConfig}etc/scram.d/qtextra.xml
%{relocateConfig}etc/scram.d/qt3support.xml
%{relocateConfig}bin/qt.conf
%{relocateConfig}mkspecs/qconfig.pri
