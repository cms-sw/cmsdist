### RPM external autotools 1.0
# We keep all of them together to simplify the "requires" statements.
%define autoconf_version 2.69
%define automake_version 1.11.4
%define libtool_version 2.4.2
%define m4_version 1.4.16
Source0: http://ftpmirror.gnu.org/autoconf/autoconf-%autoconf_version.tar.gz
Source1: http://ftpmirror.gnu.org/automake/automake-%automake_version.tar.gz
Source2: http://ftpmirror.gnu.org/libtool/libtool-%libtool_version.tar.gz
Source3: http://ftp.gnu.org/gnu/m4/m4-%m4_version.tar.bz2
Patch0: m4-1.4.16-fix-gets

%prep
%setup -D -T -b 0 -n autoconf-%{autoconf_version}
%setup -D -T -b 1 -n automake-%{automake_version}
%setup -D -T -b 2 -n libtool-%{libtool_version}
%setup -D -T -b 3 -n m4-%{m4_version}
%patch0 -p1

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
%{relocateConfig}bin/libtoolize
%{relocateConfig}share/autoconf/autom4te.cfg
%{relocateConfig}share/automake-1.11/Automake/Config.pm
