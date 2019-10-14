### RPM external rpm 4.15.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
## INITENV SET RPM_CONFIGDIR %{i}/lib/rpm
## INITENV SET RPM_POPTEXEC_PATH %{i}/bin
## NOCOMPILER

# Warning! While rpm itself seems to work, at the time of writing it
# does not seem to be possible to build apt-rpm with 
%define tag 48c04ee8077fbba1a0001968f2794cbaeb54f15c
%define branch cms/rpm-%{realversion}-release
%define github_user cms-externals
%define github_repo rpm-upstream
Source: git+https://github.com/%{github_user}/%{github_repo}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: bootstrap-bundle
BuildRequires: autotools
BuildRequires: gcc

%prep
%setup -n %{n}-%{realversion}

%build

# Reconfigure to drop pkg-config for lua
autoreconf -fiv

case %cmsplatf in
  slc*_amd64|cc*_amd64)
    CFLAGS_PLATF="-fPIC"
    LIBS_PLATF="-ldl"
  ;;
  slc*_aarch64_*|fc*)
    CFLAGS_PLATF="-fPIC"
    LIBS_PLATF="-ldl -lrt -pthread"
  ;;
  osx*)
    export CFLAGS_PLATF="-arch x86_64 -fPIC -D_FORTIFY_SOURCE=0"
    export LIBS_PLATF="-liconv"
  ;;
  *)
    export CFLAGS_PLATF="-fPIC"
  ;;
esac 

USER_CFLAGS="-ggdb -O0"
USER_CXXFLAGS="-ggdb -O0"
# On SLCx add $GCC_ROOT to various paths because that's where elflib is to be
# found.  Not required (and triggers a warning about missing include path) on
# mac.
%ifos linux
    OS_CFLAGS="-I$GCC_ROOT/include"
    OS_CXXFLAGS="-I$GCC_ROOT/include"
    OS_CPPFLAGS="-I$GCC_ROOT/include"
    OS_LDFLAGS="-L$GCC_ROOT/lib"
%endif

perl -p -i -e's|-O2|-O0|' ./configure

# Notice that libelf is now in $GCC_ROOT because also gcc LTO requires it.
./configure --prefix %{i} --build="%{_build}" --host="%{_host}" \
    --with-external-db --disable-python --disable-nls --with-archive \
    --disable-rpath --with-lua --localstatedir=%{i}/var \
    CXXFLAGS="$USER_CXXFLAGS $OS_CXXFLAGS" \
    CFLAGS="$CFLAGS_PLATF $USER_CFLAGS -I$BOOTSTRAP_BUNDLE_ROOT/include \
            $OS_CFLAGS -I/usr/include/nspr4 -I/usr/include/nss3" \
    LDFLAGS="-L$BOOTSTRAP_BUNDLE_ROOT/lib $OS_LDFLAGS" \
    CPPFLAGS="-I$BOOTSTRAP_BUNDLE_ROOT/include \
              $OS_CPPFLAGS -I/usr/include/nspr4 -I/usr/include/nss3" \
    LIBS="-lnspr4 -lnss3 -lnssutil3 -lplds4 -lbz2 -lplc4 -lz -lpopt -llzma \
          -ldb -llua -larchive $LIBS_PLATF"

#FIXME: this does not seem to work and we still get /usr/bin/python in some of the files.
export __PYTHON="/usr/bin/env python"
#perl -p -i -e "s|^.*WITH_SELINUX.*$||;
#               s|-lselinux||;
#" `find . -name \*.in` 

perl -p -i -e "s|#\!.*perl(.*)|#!/usr/bin/env perl$1|"     $(grep -R '#! */usr/bin/perl' . | sed 's|:.*||' | sort | uniq)
perl -p -i -e "s|#\!.*python(.*)|#!/usr/bin/env python$1|" $(grep -R '#! */usr/bin/python' . | sed 's|:.*||' | sort | uniq)

%install
make install
# Remove unneeded documentation
%define drop_files %i/share

# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %{i}/lib/pkgconfig
# The following patches the rpmrc to make sure that rpm macros are only picked up from
# what we distribute and not /etc or ~/
perl -p -i -e "s!:/etc/[^:]*!!g;
               s!~/[^:]*!!g" %i/lib/rpm/rpmrc

# This is for compatibility with rpm 4.3.3
perl -p -i -e "s!^.buildroot!#%%buildroot!;
               s!^%%_dbpath.*lib/rpm!%%_dbpath %{instroot}/%{cmsplatf}/var/lib/rpm!;
               s!^%%_repackage_dir.*/var/spool/repackage!%%_repackage_dir     %{instroot}/%{cmsplatf}/var/spool/repackage!" %i/lib/rpm/macros

# Removes any reference to /usr/lib/rpm in lib/rpm
perl -p -i -e 's|/usr/lib/rpm([^a-zA-Z])|%{i}/lib/rpm$1|g' \
    %{i}/lib/rpm/check-rpaths \
    %{i}/lib/rpm/check-rpaths-worker \
    %{i}/lib/rpm/find-debuginfo.sh \
    %{i}/lib/rpm/rpmdb_loadcvt \
    %{i}/lib/rpm/rpmrc \
    %{i}/lib/rpm/find-provides \
    %{i}/lib/rpm/find-requires

# Changes the shebang from /usr/bin/perl to /usr/bin/env perl
perl -p -i -e 's|^#[!]/usr/bin/perl(.*)|#!/usr/bin/env perl$1|' \
    %{i}/lib/rpm/perl.prov \
    %{i}/lib/rpm/perl.req \
    %{i}/lib/rpm/tcl.req \
    %{i}/lib/rpm/osgideps.pl

mkdir -p %{instroot}/%{cmsplatf}/var/spool/repackage

perl -p -i -e 's|.[{]prefix[}]|%instroot|g' %{i}/lib/rpm/macros

#Disabled pythondist requirement checks; we use pip checks to make sure the
#dependencies are satisfied
perl -p -i -e 's|^%%__pythondist_requires.*|%%__pythondist_requires true|' %{i}/lib/rpm/fileattrs/pythondist.attr

# Remove some of the path macros defined in macros since they could come from
# different places (e.g. from system or from macports) and this would lead to
# problems if a developer with macports builds a bootstrap package set.
for shellUtil in tar cat chgrp chmod chown cp file gpg id make mkdir mv pgp rm rsh sed ssh gzip cpio perl unzip patch grep bzip2 xz
do
    perl -p -i -e "s|^%__$shellUtil\s(.*)|%__$shellUtil       $shellUtil|" %i/lib/rpm/macros
done

ln -sf rpm %i/bin/rpmverify
ln -sf rpm %i/bin/rpmquery

mkdir -p %{i}/etc/profile.d
echo "test X\$BOOTSTRAP_BUNDLE_ROOT != X || . $BOOTSTRAP_BUNDLE_ROOT/etc/profile.d/init.sh" > %{i}/etc/profile.d/dependencies-setup.sh

%post
%{relocateRpmFiles} $(grep -I -r %cmsroot $RPM_INSTALL_PREFIX/%pkgrel | cut -d: -f1 | sort | uniq)
