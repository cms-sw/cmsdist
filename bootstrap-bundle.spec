### RPM external bootstrap-bundle 2.0
## INITENV +PATH PATH %{i}/bin
## INITENV SET MAGIC %{i}/share/misc/magic.mgc
## NOCOMPILER

BuildRequires: gcc
BuildRequires: db6-bootstrap lua-bootstrap file-bootstrap
BuildRequires: xz-bootstrap libarchive-bootstrap

%define keep_archives true

%define libdir lib64
%define soname so
%ifos darwin
%define soname dylib
%endif

%prep
%build
%install
mkdir -p %{i}/bin %{i}/lib %{i}/include %{i}/share %{i}/tmp %{i}/etc/profile.d
for tool in `echo %{buildrequiredtools} | tr ' ' '\n' | grep '\-bootstrap$'`; do
  toolcap=`echo $tool | tr a-z- A-Z_`
  toolbase=`eval echo \\$${toolcap}_ROOT`
  for sdir in bin lib include ; do
    [ -d ${toolbase}/${sdir} ] || continue
    rsync -r --links --ignore-existing ${toolbase}/${sdir}/ %{i}/${sdir}/
  done
done
mkdir %{i}/share/misc
cp ${FILE_BOOTSTRAP_ROOT}/share/misc/magic.mgc  %{i}/share/misc/magic.mgc
rm -f %{i}/bin/xml2-config %{i}/lib/xml2Conf.sh

#Bundle libstd and libgcc_s and libelf
%ifos darwin
cp -P $GCC_ROOT/lib/lib{stdc++,gcc_s}*.%{soname} %{i}/lib
%else
cp -P $GCC_ROOT/%{libdir}/lib{stdc++,gcc_s}.%{soname}* %{i}/lib
cp -P $GCC_ROOT/lib/libelf.%{soname}* %{i}/lib
cp -P $GCC_ROOT/lib/libelf-*.%{soname} %{i}/lib
cp -P $GCC_ROOT/lib/libdw.%{soname}* %{i}/lib
cp -P $GCC_ROOT/lib/libdw-*.%{soname} %{i}/lib
%endif

find %{i}/bin -type f -writable -exec %{strip} {} \;
# Do not strip archives, otherwise index of contents will be lost on newer binutils
# and an extra step (ranlib) would be required
find %{i}/lib -type f ! -name '*.a' -writable -exec %{strip} {} \;

# All shared libraries on RH/Fedora are installed with 0755
# RPM requires it to generate requires/provides also (otherwise it ignores the files)
find %{i}/lib -type f | xargs chmod 0755

mv %{i}/lib/lib{lua,archive}.a %{i}/tmp
rm -f %{i}/lib/*.{l,}a
mv %{i}/tmp/lib* %{i}/lib/
rm -rf %{i}/tmp

touch %{i}/etc/profile.d/dependencies-setup.sh  %{i}/etc/profile.d/dependencies-setup.csh

%post
rm -f $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/dependencies-setup.*
