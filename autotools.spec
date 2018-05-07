### RPM external autotools 1.4
## INITENV SET M4 %{i}/bin/m4
# We keep all of them together to simplify the "requires" statements.
%define autoconf_version 2.69
%define automake_version 1.16.1
%define automake_maj %(echo %{automake_version} | cut -f1,2 -d.)
%define libtool_version 2.4.6
%define m4_version 1.4.18
%define gettext_version 0.19.8.1
%define pkgconfig_version 0.29.2
Source0: http://ftp.gnu.org/gnu/autoconf/autoconf-%{autoconf_version}.tar.gz
Source1: http://ftp.gnu.org/gnu/automake/automake-%{automake_version}.tar.gz
Source2: http://ftp.gnu.org/gnu/libtool/libtool-%{libtool_version}.tar.gz
Source3: http://ftp.gnu.org/gnu/m4/m4-%{m4_version}.tar.bz2
Source4: http://ftp.gnu.org/gnu/gettext/gettext-%{gettext_version}.tar.gz
Source5: http://pkgconfig.freedesktop.org/releases/pkg-config-%{pkgconfig_version}.tar.gz

%prep
%setup -D -T -b 0 -n autoconf-%{autoconf_version}
%setup -D -T -b 1 -n automake-%{automake_version}
%setup -D -T -b 2 -n libtool-%{libtool_version}
%setup -D -T -b 3 -n m4-%{m4_version}
%setup -D -T -b 4 -n gettext-%{gettext_version}
%setup -D -T -b 5 -n pkg-config-%{pkgconfig_version}

# Update config.{guess,sub} scripts
rm -f %{_tmppath}/config.{sub,guess}
curl -L -k -s -o %{_tmppath}/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
curl -L -k -s -o %{_tmppath}/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
for CONFIG_GUESS_FILE in $(find $RPM_BUILD_DIR -name 'config.guess')
do
  rm -f $CONFIG_GUESS_FILE
  cp %{_tmppath}/config.guess $CONFIG_GUESS_FILE
  chmod +x $CONFIG_GUESS_FILE
done
for CONFIG_SUB_FILE in $(find $RPM_BUILD_DIR -name 'config.sub')
do
  rm -f $CONFIG_SUB_FILE
  cp %{_tmppath}/config.sub $CONFIG_SUB_FILE
  chmod +x $CONFIG_SUB_FILE
done

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
pushd %_builddir/gettext-%{gettext_version}
  ./configure --prefix %i \
              --without-xz \
              --without-bzip2 \
              --disable-curses \
              --disable-openmp \
              --enable-relocatable \
              --disable-rpath \
              --disable-nls \
              --disable-native-java \
              --disable-acl \
              --disable-java \
              --disable-dependency-tracking \
              --disable-silent-rules \
              --with-included-glib \
              --with-included-libunistring \
              --with-included-libcroco
  make %makeprocesses && make install
popd
pushd %_builddir/pkg-config-%{pkgconfig_version}
  ./configure --prefix %i \
              --disable-silent-rules \
              --disable-dependency-tracking \
              --disable-host-tool \
              --with-internal-glib \
              --disable-shared
  make %makeprocesses && make install
popd

# Fix perl location, required on /usr/bin/perl
grep -l -R '/bin/perl' %{i} | xargs -n1 sed -ideleteme -e 's;^#!.*perl;#!/usr/bin/perl;'
find %{i} -name '*deleteme' -delete
grep -l -R '/bin/perl' %{i} | xargs -n1 sed -ideleteme -e 's;exec [^ ]*/perl;exec /usr/bin/perl;g'
find %{i} -name '*deleteme' -delete

# Fix perl location, required on /usr/bin/perl
grep -l -R '/bin/perl' %{i} | xargs -n1 sed -ideleteme -e 's;^#!.*perl;#!/usr/bin/perl;'
find %{i} -name '*deleteme' -delete
grep -l -R '/bin/perl' %{i} | xargs -n1 sed -ideleteme -e 's;exec [^ ]*/perl;exec /usr/bin/perl;g'
find %{i} -name '*deleteme' -delete

%install
# NOP

%define drop_files %{i}/share/{man,doc,info}

%post
%{relocateConfig}bin/aclocal
%{relocateConfig}bin/aclocal-%{automake_maj}
%{relocateConfig}bin/autoconf
%{relocateConfig}bin/autoheader
%{relocateConfig}bin/autom4te
%{relocateConfig}bin/automake
%{relocateConfig}bin/automake-%{automake_maj}
%{relocateConfig}bin/autoreconf
%{relocateConfig}bin/autoscan
%{relocateConfig}bin/autoupdate
%{relocateConfig}bin/ifnames
%{relocateConfig}bin/libtoolize
%{relocateConfig}share/autoconf/autom4te.cfg
%{relocateConfig}share/automake-%{automake_maj}/Automake/Config.pm
%{relocateConfig}bin/gettextize
%{relocateConfig}lib/gettext/user-email
%{relocateConfig}bin/autopoint
