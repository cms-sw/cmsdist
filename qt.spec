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
cat << \EOF_TOOLFILE >%i/etc/scram.d/qtbase
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=qtbase version=%v>
<info url="http://www.trolltech.com/products/qt.html"></info>
<LIB name=QtCore>
<LIB name=QtXml>
<Client>
 <Environment name=QT_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$QT_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/Qt"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtCore"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtXml"></Environment>
</Client>
<Flags CPPDEFINES="QT_ALTERNATE_QTSMANIP QT_CLEAN_NAMESPACE QT_THREAD_SUPPORT">
<Runtime name=PATH value="$QT_BASE/bin" type=path>
<use name=zlib>
</Tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qt3support
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=qt3support version=%v>
<info url="http://www.trolltech.com/products/qt.html"></info>
<LIB name=Qt3Support>
<Client>
 <Environment name=QT_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/Qt3Support"></Environment>
</Client>
<Flags CPPDEFINES="QT3_SUPPORT">
<use name=qtbase>
</Tool>
EOF_TOOLFILE


cat << \EOF_TOOLFILE >%i/etc/scram.d/qt
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=qt version=%v>
<info url="http://www.trolltech.com/products/qt.html"></info>
<LIB name=QtOpenGL>
<LIB name=QtGui>
<Client>
 <Environment name=QT_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtOpenGL"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtGui"></Environment>
</Client>
<use name=qtbase>
<use name=qt3support>
<use name=X11>
<use name=opengl>
</Tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qtdesigner
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=qtdesigner version=%v>
<info url="http://www.trolltech.com/products/qt.html"></info>
<LIB name=QtDesigner>
<Client>
 <Environment name=QT_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtDesigner"></Environment>
</Client>
<use name=qtbase>
<use name=qt>
</Tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qtextra
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=qtextra version=%v>
<info url="http://www.trolltech.com/products/qt.html"></info>
<LIB name=QtScript>
<Client>
 <Environment name=QT_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtScript"></Environment>
</Client>
<use name=qtbase>
</Tool>
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
%{relocateConfig}etc/scram.d/qtbase
%{relocateConfig}etc/scram.d/qt
%{relocateConfig}etc/scram.d/qtdesigner
%{relocateConfig}etc/scram.d/qtextra
%{relocateConfig}etc/scram.d/qt3support
%{relocateConfig}bin/qt.conf
