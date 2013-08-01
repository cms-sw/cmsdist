### RPM external autotools 1.0
# We keep all of them together to simplify the "requires" statements.
%define autoconf_version 2.68
%define automake_version 1.11.4
%define libtool_version 2.4.2
%define m4_version 1.4.16
Source0: http://ftpmirror.gnu.org/autoconf/autoconf-%autoconf_version.tar.gz
Source1: http://ftpmirror.gnu.org/automake/automake-%automake_version.tar.gz
Source2: http://ftpmirror.gnu.org/libtool/libtool-%libtool_version.tar.gz
Source3: http://ftp.gnu.org/gnu/m4/m4-%m4_version.tar.bz2

%prep
%setup -D -T -b 0 -n autoconf-%{autoconf_version}
%setup -D -T -b 1 -n automake-%{automake_version}
%setup -D -T -b 2 -n libtool-%{libtool_version}
%setup -D -T -b 3 -n m4-%{m4_version}

%build
export PATH=%i/bin:$PATH
pushd %_builddir/m4-%{m4_version} 
  ./configure --disable-dependency-tracking --prefix %i
  make %makeprocesses && make install
popd
pushd %_builddir/autoconf-%{autoconf_version}
  ./configure --disable-dependency-tracking --prefix %i
  make %makeprocesses && make install
popd
pushd %_builddir/automake-%{automake_version}
  ./configure --disable-dependency-tracking --prefix %i
  make %makeprocesses && make install
popd
pushd %_builddir/libtool-%{libtool_version} 
  ./configure --disable-dependency-tracking --prefix %i --enable-ltdl-install
  make %makeprocesses && make install
popd

%install
echo "Foo"
%post
%{relocateRpmPkg}bin/aclocal
%{relocateRpmPkg}bin/aclocal-1.11
%{relocateRpmPkg}bin/autoconf
%{relocateRpmPkg}bin/autoheader
%{relocateRpmPkg}bin/autom4te
%{relocateRpmPkg}bin/automake
%{relocateRpmPkg}bin/automake-1.11
%{relocateRpmPkg}bin/autoreconf
%{relocateRpmPkg}bin/autoscan
%{relocateRpmPkg}bin/autoupdate
%{relocateRpmPkg}bin/ifnames
%{relocateRpmPkg}bin/libtoolize
%{relocateRpmPkg}share/autoconf/autom4te.cfg
%{relocateRpmPkg}share/automake-1.11/Automake/ChannelDefs.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Channels.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Condition.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Config.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Configure_ac.pm
%{relocateRpmPkg}share/automake-1.11/Automake/DisjConditions.pm
%{relocateRpmPkg}share/automake-1.11/Automake/FileUtils.pm
%{relocateRpmPkg}share/automake-1.11/Automake/General.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Getopt.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Item.pm
%{relocateRpmPkg}share/automake-1.11/Automake/ItemDef.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Location.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Options.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Rule.pm
%{relocateRpmPkg}share/automake-1.11/Automake/RuleDef.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Struct.pm
%{relocateRpmPkg}share/automake-1.11/Automake/VarDef.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Variable.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Version.pm
%{relocateRpmPkg}share/automake-1.11/Automake/Wrap.pm
%{relocateRpmPkg}share/automake-1.11/Automake/XFile.pm
