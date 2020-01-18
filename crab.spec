### RPM cms crab 1.0
## NOCOMPILER
## NO_AUTO_DEPENDENCY
Requires: crab-prod crab-pre crab-dev

#Crab startup script which finds latest crab client, sets env and run it
Source0: crab/crab.sh
#Needed for CRAB Python API
Source1: crab/crab-proxy-package
#CRAB Setup script
Source2: crab/crab-setup.csh
Source3: crab/crab-setup.sh
#CRAB env script
Source4: crab/crab-env.csh
Source5: crab/crab-env.sh

%define copy_revision_file() \
  OLD_REV=0 \
  if [ -f %2 ] ; then OLD_REV=$(grep '^\s*#\s*CMSDIST_FILE_REVISION\s*=' %{2} | tail -1 | sed 's|.*=||;s| ||g') ; fi \
  NEW_REV=$(grep '^\s*#\s*CMSDIST_FILE_REVISION\s*=' %{1} | tail -1 | sed 's|.*=||;s| ||g') \
  if [ ${OLD_REV} -lt ${NEW_REV} ] ; then rm -f %2 ; cp %1 %2 ; fi

%prep
%build
%install

#Copy scripts needed for crab startup and api
cp %{_sourcedir}/crab-proxy-package %{i}/
cp %{_sourcedir}/crab.sh            %{i}/
cp %{_sourcedir}/crab-env.*sh       %{i}/
cp %{_sourcedir}/crab-setup.*sh     %{i}/
chmod +x %{i}/crab.sh
sed -i -e 's|@CMS_PATH@|%{cmsroot}|g' %{i}/crab*
sed -i -e 's|@CRAB_COMMON_VERSION@|%{realversion}|g' %{i}/crab*

%post
%{relocateConfig}/crab*

cd ${RPM_INSTALL_PREFIX}
crab=share/%{pkgcategory}/%{n}/%{realversion}
mkdir -p ${crab}/bin ${crab}/lib ${crab}/etc share/etc/profile.d
for f in crab-env.csh crab-env.sh ; do
  %copy_revision_file %{pkgrel}/$f share/etc/profile.d/S99$f
done
for f in crab-setup.csh crab-setup.sh ; do
  %copy_revision_file %{pkgrel}/$f common/$f
done
%copy_revision_file %{pkgrel}/crab.sh            ${crab}/bin/crab.sh
%copy_revision_file %{pkgrel}/crab-proxy-package ${crab}/lib/crab-proxy-package

for pkg in $(echo %{directpkgreqs} | tr ' ' '\n' | grep '^cms/crab-') ; do
  crab_name=$(echo $pkg | cut -d/ -f2)
  crab_type=$(echo $crab_name | sed -e 's|^crab-||')
  for p in $(cat share/${pkg}/etc/crab_py_pkgs.txt); do
    mkdir -p ${crab}/lib/${crab_type}/$p
    rm -rf ${crab}/lib/${crab_type}/$p/__init__.py*
    ln -s ../../crab-proxy-package ${crab}/lib/${crab_type}/$p/__init__.py
  done
  #Find latest version; extra .zzzz are added so that version 3.3.2001 becomes > 3.3.2001.rcX
  ls -d share/cms/${crab_name}/*/bin/crab | sed -e 's|/bin/crab$|.zzzz|;s|.*/||' | sort -n | sed -e 's|.zzzz$||' | tail -1 > ${crab}/etc/${crab_name}.latest
  rm -f common/_crab-startup common/${crab_name}
  ln -s ../${crab}/bin/crab.sh common/${crab_name}
done
