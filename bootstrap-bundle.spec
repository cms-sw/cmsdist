### RPM external bootstrap-bundle 5.0
## NO_AUTO_DEPENDENCY
## NOCOMPILER
AutoReqProv: no
BuildRequires: gcc
BuildRequires: lua-bootstrap file-bootstrap zstd-bootstrap
BuildRequires: xz-bootstrap libarchive-bootstrap sqlite-bootstrap

%define keep_archives true

%define libdir lib64
%define soname so
%ifos darwin
%define soname dylib
%endif

%prep
%build
%install
TOOL_LIBS="zstd:zstd sqlite:sqlite3 libarchive:archive zlib:z xz:lzma libelf:elf"
PKG_TOOL_FILE="zstd:libzstd sqlite:sqlite3 xz:liblzma"
PKG_TOOL_NAME="sqlite:SQLite xz:liblzma"
mkdir -p %{i}/bin %{i}/lib %{i}/include %{i}/share %{i}/tmp %{i}/etc/profile.d %{i}/pkgconfig
for tool in `echo %{buildrequiredtools} | tr ' ' '\n' | grep '\-bootstrap$'`; do
  toolcap=`echo $tool | tr a-z- A-Z_`
  toolbase=`eval echo \\$${toolcap}_ROOT`
  tool_name=$(echo $tool | sed 's|-bootstrap$||')
  toolver=`echo %{allpkgreqs} | tr ' ' '\n' | grep "$tool" | cut -d/ -f3 | sed -E -e 's|-[a-f0-9]{32}$||'`
  for sdir in bin lib include ; do
    [ -d ${toolbase}/${sdir} ] || continue
    rsync -r --links --ignore-existing ${toolbase}/${sdir}/ %{i}/${sdir}/
  done
  tool_lib=$(echo ${TOOL_LIBS} | tr ' ' '\n' | grep "^${tool_name}:" | sed 's|.*:||')
  [ "${tool_lib}" = "" ] && tool_lib="${tool_name}"
  tool_libs=""
  for l in $(echo $tool_lib | tr ',' ' ') ; do
    #if [ -e "${toolbase}/lib/lib${l}.a" ] ; then
    #  tool_libs="${tool_libs} ${toolbase}/lib/lib${l}.a"
    #else
      tool_libs="${tool_libs} -l${l}"
    #fi
  done
  pkg_tool_file=$(echo ${PKG_TOOL_FILE} | tr ' ' '\n' | grep "^${tool_name}:" | sed 's|.*:||')
  pkg_tool_name=$(echo ${PKG_TOOL_NAME} | tr ' ' '\n' | grep "^${tool_name}:" | sed 's|.*:||')
  [ "${tool_lib}" = "" ] && tool_lib="-l${tool_name}"
  [ "${pkg_tool_name}" = "" ] && pkg_tool_name=${tool_name}
  [ "${pkg_tool_file}" = "" ] && pkg_tool_file=${tool_name}
  cat >%{i}/pkgconfig/${pkg_tool_file}.pc <<EOL
prefix=%{i}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: ${pkg_tool_name}
Description: CMS Pakcage ${pkg_tool_name}
Version: ${toolver}
Libs: -L\${libdir} ${tool_libs}
Cflags: -I\${includedir}
EOL
done

cat >%{i}/pkgconfig/libdw.pc <<EOL
prefix=%{i}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: libdw
Description: CMS Pakcage libdw
Version: 0.0
Libs: -L\${libdir} -ldw
Cflags: -I\${includedir}
EOL

cat >%{i}/pkgconfig/libelf.pc <<EOL
prefix=%{i}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: libelf
Description: CMS Pakcage libelf
Version: 0.0
Libs: -L\${libdir} -lelf
Cflags: -I\${includedir}
EOL

mkdir %{i}/share/misc
cp ${FILE_BOOTSTRAP_ROOT}/share/misc/magic.mgc  %{i}/share/misc/magic.mgc
rm -f %{i}/bin/xml2-config %{i}/lib/xml2Conf.sh

%if 0%{!?use_system_gcc:1}
#Bundle libstd and libgcc_s and libelf
cp -P $GCC_ROOT/%{libdir}/lib{stdc++,gcc_s}.%{soname}* %{i}/lib
cp -P $GCC_ROOT/lib/libelf.%{soname}* %{i}/lib
cp -P $GCC_ROOT/lib/libelf-*.%{soname} %{i}/lib
cp -P $GCC_ROOT/lib/libdw.%{soname}* %{i}/lib
cp -P $GCC_ROOT/lib/libdw-*.%{soname} %{i}/lib
cp -P $GCC_ROOT/bin/readelf %{i}/bin
%endif

find %{i}/bin -type f -writable -exec %{strip} {} \;
# Do not strip archives, otherwise index of contents will be lost on newer binutils
# and an extra step (ranlib) would be required
find %{i}/lib -type f ! -name '*.a' -writable -exec %{strip} {} \;

# All shared libraries on RH/Fedora are installed with 0755
# RPM requires it to generate requires/provides also (otherwise it ignores the files)
find %{i}/lib -type f | xargs chmod 0755

mv %{i}/lib/lib{lua,archive,zstd,lzma,magic}.a %{i}/tmp
rm -f %{i}/lib/*.{l,}a
mv %{i}/tmp/lib* %{i}/lib/
rm -rf %{i}/tmp

%post
%{relocateConfig}pkgconfig/*.pc
