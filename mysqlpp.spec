### RPM external mysqlpp 1.7.40
# Local patches and build system fudging by Lassi A. Tuura <lat@iki.fi>
# FIXME: zlib usage?

%if "%cmsplatf" != "slc4onl_ia32_gcc346"
Requires: mysql zlib
%endif

%define downloadn mysql++
Source: http://tangentsoft.net/%{downloadn}/releases/%{downloadn}-%realversion.tar.gz
Patch0: mysqlpp-macosx
Patch1: mysqlpp-1.7.40-gcc43

%prep
%setup -n %{downloadn}-%realversion
# The following is actually a gcc4 patch
%ifos darwin
%patch0 -p1
%endif
%patch1 -p2
rm -f config.status
[ $(uname) = Darwin ] && cp /usr/share/libtool/config.* .

%build
%if "%cmsplatf" != "slc4onl_ia32_gcc346"
echo "ZLIB_ROOT" $ZLIB_ROOT
export CPPFLAGS=-I$ZLIB_ROOT/include
export LDFLAGS=-L$ZLIB_ROOT/lib
./configure --prefix=%i \
            --with-mysql=$MYSQL_ROOT \
            --with-mysql-lib=$MYSQL_ROOT/lib/mysql \
            --with-mysql-include=$MYSQL_ROOT/include/mysql
%else
./configure --prefix=%i
%endif
perl -p -i -e 's/\@OBJEXT\@/o/g; s/\@EXEEXT\@//g' examples/Makefile
make
#

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <lib name="mysqlpp"/>
    <client>
      <environment name="MYSQLPP_BASE" default="%i"/>
      <environment name="LIBDIR" default="$MYSQLPP_BASE/lib"/>
      <environment name="INCLUDE" default="$MYSQLPP_BASE/include"/>
    </client>
    <use name="mysql"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
