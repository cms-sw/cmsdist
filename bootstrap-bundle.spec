### RPM external bootstrap-bundle 1.0
## INITENV SET MAGIC %{i}/share/magic.mgc
## NOCOMPILER

BuildRequires: gcc
BuildRequires: bz2lib-bootstrap db4-bootstrap file-bootstrap libxml2-bootstrap lua-bootstrap nspr-bootstrap nss-bootstrap
BuildRequires: openssl-bootstrap popt-bootstrap sqlite-bootstrap zlib-bootstrap

%define keep_archives true
%define ismac   %(case %{cmsplatf} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%if %ismac
%define soname dylib
%else
%define soname so
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
cp -r ${FILE_BOOTSTRAP_ROOT}/share/misc/magic.mgc %{i}/share
rm -f %{i}/bin/xml2-config %{i}/lib/xml2Conf.sh

#Bundle libstd and libgcc_s and libelf
%if %ismac
cp -P $GCC_ROOT/lib/lib{stdc++,gcc_s}*.%{soname} %{i}/lib
%else
cp -P $GCC_ROOT/lib64/lib{stdc++,gcc_s}.%{soname}* %{i}/lib
cp -P $GCC_ROOT/lib/libelf.%{soname}* %{i}/lib
cp -P $GCC_ROOT/lib/libelf-*.%{soname} %{i}/lib
%endif

find %{i}/bin -type f -perm -a+x -exec %strip {} \;
find %{i}/lib -type f -perm -a+x -exec %strip {} \;

mv %{i}/lib/lib{lua,magic}.a %{i}/tmp
rm -f %{i}/lib/*.{l,}a
mv %{i}/tmp/lib* %{i}/lib/
rm -rf %{i}/tmp
