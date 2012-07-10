### RPM external autotools 1.0
# We keep all of them together to simplify the "requires" statements.
%define autoconf_version 2.68
%define automake_version 1.11.4
%define libtool_version 2.4.2
Source0: http://ftpmirror.gnu.org/autoconf/autoconf-%autoconf_version.tar.gz
Source1: http://ftpmirror.gnu.org/automake/automake-%automake_version.tar.gz
Source2: http://ftpmirror.gnu.org/libtool/libtool-%libtool_version.tar.gz

%prep
%setup -D -T -b 0 -n autoconf-%{autoconf_version}
%setup -D -T -b 1 -n automake-%{automake_version}
%setup -D -T -b 2 -n libtool-%{libtool_version}

%build
pushd %_builddir/autoconf-%{autoconf_version}
  ./configure --disable-dependency-tracking --prefix %i
  make %makeprocesses
popd
pushd %_builddir/automake-%{automake_version}
  ./configure --disable-dependency-tracking --prefix %i
  make %makeprocesses
popd
pushd %_builddir/libtool-%{libtool_version} 
  ./configure --disable-dependency-tracking --prefix %i --enable-ltdl-install
  make %makeprocesses
popd
%install
pushd %_builddir/autoconf-%{autoconf_version}
  make install
popd
pushd %_builddir/automake-%{automake_version}
  make install
popd
pushd %_builddir/libtool-%{libtool_version} 
  make install
popd