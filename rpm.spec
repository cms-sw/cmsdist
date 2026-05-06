### RPM external rpm 4.20.1
## INITENV SET RPM_CONFIGDIR %{i}/libx/rpm
## INITENV SET RPM_POPTEXEC_PATH %{i}/bin
## INITENV SET MAGIC %{i}/share/misc/magic.mgc
## INITENV SET CMSPKG_RPM_OPTS --noplugins
## NOCOMPILER
## NO_AUTO_DEPENDENCY
AutoReqProv: no
%define tag 3ff2d9bf5a5562eb5d2428a905b73405b650eae0
%define branch cms/rpm-%{realversion}-release
%define github_user cms-externals
%define github_repo rpm-upstream
Source: git+https://github.com/%{github_user}/%{github_repo}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Source2: rpm-set_runpath

BuildRequires: gcc
BuildRequires: bootstrap-bundle patchelf-bootstrap
BuildRequires: zstd-bootstrap xz-bootstrap libarchive-bootstrap

%prep
%setup -n %{n}-%{realversion}

%build

rm -rf ../build; mkdir ../build ; cd ../build
#which cmake
export PKG_CONFIG_PATH=${BOOTSTRAP_BUNDLE_ROOT}/pkgconfig:/usr/share/pkgconfig:/usr/lib/pkgconfig:/usr/lib64/pkgconfig
#export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1
#export PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
#export PKG_CONFIG_STATIC=1
#export PKG_CONFIG_EXECUTABLE=`which pkg-config`
cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX="%{i}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DLUA_Debug=ON \
  -DCMAKE_SKIP_RPATH=ON \
  -DENABLE_CUTF8=OFF \
  -DENABLE_NLS=ON \
  -DENABLE_OPENMP=OFF \
  -DENABLE_PYTHON=OFF \
  -DENABLE_WERROR=OFF \
  -DENABLE_SQLITE=ON \
  -DENABLE_NDB=ON \
  -DENABLE_BDB_RO=OFF \
  -DENABLE_TESTSUITE=OFF \
  -DENABLE_ASAN=OFF \
  -DENABLE_UBSAN=OFF \
  -DWITH_CAP=OFF \
  -DWITH_ACL=OFF \
  -DWITH_AUDIT=OFF \
  -DWITH_SEQUOIA=OFF \
  -DWITH_SELINUX=OFF \
  -DWITH_DBUS=OFF \
  -DWITH_OPENSSL=ON \
  -DWITH_READLINE=ON \
  -DWITH_ICONV=OFF \
  -DWITH_BZIP2=ON \
  -DWITH_LIBDW=ON \
  -DWITH_LIBELF=ON \
  -DWITH_ZSTD=ON \
  -DWITH_LIBLZMA=ON \
  -DWITH_DOXYGEN=OFF \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_EXE_LINKER_FLAGS="-static-libgcc -static-libstdc++ -lbz2 -lz -llzma" \
  -DCMAKE_PREFIX_PATH="${BOOTSTRAP_BUNDLE_ROOT}"

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make install

# Remove unneeded documentation
rm -rf %i/share

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
perl -p -i -e 's|/usr/lib/rpm([^a-zA-Z])|%{i}/libx/rpm$1|g' \
    %{i}/lib/rpm/check-rpaths \
    %{i}/lib/rpm/check-rpaths-worker \
    %{i}/lib/rpm/find-debuginfo.sh \
    %{i}/lib/rpm/rpmdb_loadcvt \
    %{i}/lib/rpm/rpmrc \
    %{i}/lib/rpm/find-provides \
    %{i}/lib/rpm/find-requires

#Fix vendor
grep -ElR '_vendor\s+vendor' %{i}/lib/rpm/platform | xargs perl -p -i -e 's|(_vendor\s+)vendor|${1}redhat|'
perl -p -i -e 's|(_vendor\s+)vendor|${1}redhat|'  %{i}/lib/rpm/macros

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

#rpath settings
#Copy bootstrap/patchelf lib
mv %{i}/lib %{i}/libx
cp -rf $BOOTSTRAP_BUNDLE_ROOT/bin/* %{i}/bin
cp -f $PATCHELF_BOOTSTRAP_ROOT/bin/patchelf %{i}/bin
cp %{_sourcedir}/rpm-set_runpath %{i}/bin/set_runpath
chmod +x %{i}/bin/set_runpath
#Copy bootstrap share/lib
cp -rf $BOOTSTRAP_BUNDLE_ROOT/share %i/share
cp -rf $BOOTSTRAP_BUNDLE_ROOT/lib/* %{i}/libx

MAGIC=%{i}/share/misc/magic.mgc  %{dynamic_path_var}=%{i}/libx PATH="%{i}/bin:${PATH}" \
  %{i}/bin/set_runpath --prefix %{cmsroot}/%{cmsplatf} --package %{i} \
  --force-rpath --rpath '$ORIGIN:$ORIGIN/..:$ORIGIN/../lib64:$ORIGIN/../libx' --jobs %{compiling_processes}
MAGIC=%{i}/share/misc/magic.mgc  %{dynamic_path_var}=%{i}/libx PATH="%{i}/bin:${PATH}" \
  %{i}/bin/set_runpath --prefix %{cmsroot}/%{cmsplatf} --package %{i} -M libx/rpm \
  --force-rpath --rpath '$ORIGIN::$ORIGIN/../../lib64:$ORIGIN/../../libx' --jobs %{compiling_processes}

#Create lib/rpm
mkdir -p %{i}/lib
for d in lua rpm rpm-plugins ; do ln -sf ../libx/$d %{i}/lib/$d ; done

%post
%{relocateRpmFiles} $(grep -I -r %cmsroot $RPM_INSTALL_PREFIX/%pkgrel | cut -d: -f1 | grep -v '/%pkgrel/etc/profile.d/' | sort | uniq)
