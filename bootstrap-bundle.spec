### RPM external bootstrap-bundle 1.0
## NOCOMPILER

BuildRequires: gcc
BuildRequires: bz2lib-bootstrap db4-bootstrap file-bootstrap libxml2-bootstrap lua-bootstrap nspr-bootstrap nss-bootstrap
BuildRequires: openssl-bootstrap popt-bootstrap sqlite-bootstrap zlib-bootstrap xz-bootstrap

%define keep_archives true
%define isamd64 %(case %{cmsplatf} in (*amd64*|*_mic_*) echo 1 ;; (*) echo 0 ;; esac)
%define ismac   %(case %{cmsplatf} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%define soname so
%if %ismac
%define soname dylib
%endif

%define libdir lib
%if %isamd64
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

find %{i}/bin -type f -perm -a+x -exec %strip {} \;
find %{i}/lib -type f -perm -a+x -exec %strip {} \;

mv %{i}/lib/lib{lua,magic}.a %{i}/tmp
rm -f %{i}/lib/*.{l,}a
mv %{i}/tmp/lib* %{i}/lib/
rm -rf %{i}/tmp
rm -rf %{i}/bin/file

%if %ismac
for file in %{i}/lib/*.dylib*;do
    chmod u+w $file
    for dep in `otool -L $file | sed -e's|(.*||' | grep -v -e':$'`;do
       if [ -z "${dep##@*path/*}" ]; then
         newdep="@loader_path/"`basename $dep`
         install_name_tool -change $dep $newdep $file || true
       fi
    done
    for RP in `otool -l $file | grep -A3 LC_RP | grep path | awk '{print $2}'`;do
       if [ -z "${RP##*/*}" ]; then
         install_name_tool -delete_rpath $RP $file || true
       fi
    done
    chmod u-w $file
done
for file in %{i}/bin/*;do
    chmod u+w $file
    for dep in `otool -L $file | sed -e's|(.*||' | grep -v -e':$'`;do
       if [ -z "${dep##@*path/*}" ]; then
         newdep="@executable_path/../lib/"`basename $dep`
         install_name_tool -change $dep $newdep $file || true
       fi
    done
    for RP in `otool -l $file | grep -A3 LC_RP | grep path | awk '{print $2}'`;do
       if [ -z "${RP##@*/*}" ]; then
         install_name_tool -delete_rpath $RP $file || true
       fi
    done
    chmod u-w $file
done
%endif
