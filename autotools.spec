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
%{relocateConfig}bin/aclocal
%{relocateConfig}bin/aclocal-1.11
%{relocateConfig}bin/autoconf
%{relocateConfig}bin/autoheader
%{relocateConfig}bin/autom4te
%{relocateConfig}bin/automake
%{relocateConfig}bin/automake-1.11
%{relocateConfig}bin/autoreconf
%{relocateConfig}bin/autoscan
%{relocateConfig}bin/autoupdate
%{relocateConfig}bin/ifnames
%{relocateConfig}bin/libtool
%{relocateConfig}bin/libtoolize
%{relocateConfig}bin/m4
%{relocateConfig}share/autoconf/autom4te.cfg
%{relocateConfig}share/automake-1.11/Automake/ChannelDefs.pm
%{relocateConfig}share/automake-1.11/Automake/Channels.pm
%{relocateConfig}share/automake-1.11/Automake/Condition.pm
%{relocateConfig}share/automake-1.11/Automake/Config.pm
%{relocateConfig}share/automake-1.11/Automake/Configure_ac.pm
%{relocateConfig}share/automake-1.11/Automake/DisjConditions.pm
%{relocateConfig}share/automake-1.11/Automake/FileUtils.pm
%{relocateConfig}share/automake-1.11/Automake/General.pm
%{relocateConfig}share/automake-1.11/Automake/Getopt.pm
%{relocateConfig}share/automake-1.11/Automake/Item.pm
%{relocateConfig}share/automake-1.11/Automake/ItemDef.pm
%{relocateConfig}share/automake-1.11/Automake/Location.pm
%{relocateConfig}share/automake-1.11/Automake/Options.pm
%{relocateConfig}share/automake-1.11/Automake/Rule.pm
%{relocateConfig}share/automake-1.11/Automake/RuleDef.pm
%{relocateConfig}share/automake-1.11/Automake/Struct.pm
%{relocateConfig}share/automake-1.11/Automake/VarDef.pm
%{relocateConfig}share/automake-1.11/Automake/Variable.pm
%{relocateConfig}share/automake-1.11/Automake/Version.pm
%{relocateConfig}share/automake-1.11/Automake/Wrap.pm
%{relocateConfig}share/automake-1.11/Automake/XFile.pm
%{relocateConfig}share/autoconf/Autom4te/C4che.pm
%{relocateConfig}share/autoconf/Autom4te/ChannelDefs.pm
%{relocateConfig}share/autoconf/Autom4te/Channels.pm
%{relocateConfig}share/autoconf/Autom4te/Configure_ac.pm
%{relocateConfig}share/autoconf/Autom4te/FileUtils.pm
%{relocateConfig}share/autoconf/Autom4te/General.pm
%{relocateConfig}share/autoconf/Autom4te/Request.pm
%{relocateConfig}share/autoconf/Autom4te/Struct.pm
%{relocateConfig}share/autoconf/Autom4te/XFile.pm
%{relocateConfig}share/aclocal-1.11/amversion.m4
%{relocateConfig}share/aclocal-1.11/ar-lib.m4
%{relocateConfig}share/aclocal-1.11/as.m4
%{relocateConfig}share/aclocal-1.11/auxdir.m4
%{relocateConfig}share/aclocal-1.11/ccstdc.m4
%{relocateConfig}share/aclocal-1.11/cond-if.m4
%{relocateConfig}share/aclocal-1.11/cond.m4
%{relocateConfig}share/aclocal-1.11/depend.m4
%{relocateConfig}share/aclocal-1.11/depout.m4
%{relocateConfig}share/aclocal-1.11/dmalloc.m4
%{relocateConfig}share/aclocal-1.11/gcj.m4
%{relocateConfig}share/aclocal-1.11/header.m4
%{relocateConfig}share/aclocal-1.11/init.m4
%{relocateConfig}share/aclocal-1.11/install-sh.m4
%{relocateConfig}share/aclocal-1.11/lead-dot.m4
%{relocateConfig}share/aclocal-1.11/lex.m4
%{relocateConfig}share/aclocal-1.11/lispdir.m4
%{relocateConfig}share/aclocal-1.11/maintainer.m4
%{relocateConfig}share/aclocal-1.11/make.m4
%{relocateConfig}share/aclocal-1.11/minuso.m4
%{relocateConfig}share/aclocal-1.11/missing.m4
%{relocateConfig}share/aclocal-1.11/mkdirp.m4
%{relocateConfig}share/aclocal-1.11/multi.m4
%{relocateConfig}share/aclocal-1.11/obsol-gt.m4
%{relocateConfig}share/aclocal-1.11/obsol-lt.m4
%{relocateConfig}share/aclocal-1.11/obsolete.m4
%{relocateConfig}share/aclocal-1.11/options.m4
%{relocateConfig}share/aclocal-1.11/protos.m4
%{relocateConfig}share/aclocal-1.11/python.m4
%{relocateConfig}share/aclocal-1.11/regex.m4
%{relocateConfig}share/aclocal-1.11/runlog.m4
%{relocateConfig}share/aclocal-1.11/sanity.m4
%{relocateConfig}share/aclocal-1.11/silent.m4
%{relocateConfig}share/aclocal-1.11/strip.m4
%{relocateConfig}share/aclocal-1.11/substnot.m4
%{relocateConfig}share/aclocal-1.11/tar.m4
%{relocateConfig}share/aclocal-1.11/upc.m4
%{relocateConfig}share/aclocal-1.11/vala.m4
