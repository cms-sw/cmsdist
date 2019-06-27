### RPM external qt-toolfile 1.0
Requires: qt
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/qtbase.xml
<tool name="qtbase" version="@TOOL_VERSION@">
  <info url="http://qt-project.org"/>
  <lib name="QtCore"/>
  <lib name="QtXml"/>
  <client>
    <environment name="QTBASE_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$QTBASE_BASE/lib"/>
    <environment name="INCLUDE" default="$QTBASE_BASE/include"/>
    <environment name="INCLUDE" default="$QTBASE_BASE/include/Qt"/>
    <environment name="INCLUDE" default="$QTBASE_BASE/include/QtCore"/>
    <environment name="INCLUDE" default="$QTBASE_BASE/include/QtXml"/>
  </client>
  <flags cppdefines="QT_ALTERNATE_QTSMANIP QT_CLEAN_NAMESPACE QT_THREAD_SUPPORT"/>
  <runtime name="PATH" value="$QTBASE_BASE/bin" type="path"/>
  <runtime name="QTDIR" value="$QTBASE_BASE" type="path"/>
  <runtime name="QTINC" value="$QTBASE_BASE/include" type="path"/>
  <runtime name="QTLIB" value="$QTBASE_BASE/lib" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$QTBASE_BASE/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$QTBASE_BASE/include/Qt" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$QTBASE_BASE/include/QtCore" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$QTBASE_BASE/include/QtXml" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qt3support.xml
<tool name="qt3support" version="@TOOL_VERSION@">
  <info url="http://qt-project.org"/>
  <lib name="Qt3Support"/>
  <client>
    <environment name="QT3SUPPORT_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$QT3SUPPORT_BASE/include/Qt3Support"/>
  </client>
  <flags cppdefines="QT3_SUPPORT"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$QT3SUPPORT_BASE/include/Qt3Support" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="qtbase"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qt.xml
<tool name="qt" version="@TOOL_VERSION@">
  <info url="http://qt-project.org"/>
  <lib name="QtOpenGL"/>
  <lib name="QtGui"/>
  <client>
    <environment name="QT_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$QT_BASE/include/QtOpenGL"/>
    <environment name="INCLUDE" default="$QT_BASE/include/QtGui"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$QT_BASE/include/QtOpenGL" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$QT_BASE/include/QtGui" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="qtbase"/>
  <use name="qt3support"/>
  <use name="X11"/>
  <use name="opengl"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qtdesigner.xml
<tool name="qtdesigner" version="@TOOL_VERSION@">
  <info url="http://qt-project.org"/>
  <lib name="QtDesigner"/>
  <client>
    <environment name="QTDESIGNER_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$QTDESIGNER_BASE/include/QtDesigner"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$QTDESIGNER_BASE/include/QtDesigner" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="qtbase"/>
  <use name="qt"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
