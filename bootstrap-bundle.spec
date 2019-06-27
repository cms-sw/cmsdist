### RPM external bootstrap-bundle 1.7
## INITENV +PATH PATH %{i}/bin
## NOCOMPILER

BuildRequires: gcc
BuildRequires: db6-bootstrap libxml2-bootstrap lua-bootstrap
BuildRequires: openssl-bootstrap xz-bootstrap libarchive-bootstrap

%define keep_archives true
%define is64bit %(case %{cmsplatf} in (*_amd64_*|*_mic_*|*_aarch64_*|*_ppc64le_*|*_ppc64_*) echo 1 ;; (*) echo 0 ;; esac)
%define ismac   %(case %{cmsplatf} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%define soname so
%if %ismac
%define soname dylib
%endif

%define libdir lib
%if %is64bit
%define libdir lib64
%endif

%prep
%build
%install
mkdir %{i}/bin %{i}/lib %{i}/include %{i}/share %{i}/tmp
for tool in `echo %{buildrequiredtools} | tr ' ' '\n' | grep '\-bootstrap$'`; do
  toolcap=`echo $tool | tr a-z- A-Z_`
  toolbase=`eval echo \\$${toolcap}_ROOT`
  for sdir in bin lib include ; do
    [ -d ${toolbase}/${sdir} ] || continue
    rsync -r --links --ignore-existing ${toolbase}/${sdir}/ %{i}/${sdir}/
  done
done
rm -f %{i}/bin/xml2-config %{i}/lib/xml2Conf.sh

#Bundle libstd and libgcc_s and libelf
%if %ismac
cp -P $GCC_ROOT/lib/lib{stdc++,gcc_s}*.%{soname} %{i}/lib
%else
cp -P $GCC_ROOT/%{libdir}/lib{stdc++,gcc_s}.%{soname}* %{i}/lib
cp -P $GCC_ROOT/lib/libelf.%{soname}* %{i}/lib
cp -P $GCC_ROOT/lib/libelf-*.%{soname} %{i}/lib
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
# bla bla
