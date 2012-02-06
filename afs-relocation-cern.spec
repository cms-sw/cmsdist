### RPM cms afs-relocation-cern 1.0
## REVISION 102
## NOCOMPILER
%define CmsRelocationDir  /afs/cern.ch/cms
%prep
%build
%install

mkdir -p %instroot/common
echo 'CMS_INSTALL_PREFIX="%{CmsRelocationDir}"; export CMS_INSTALL_PREFIX' > %instroot/common/apt-site-env.sh
echo "setenv CMS_INSTALL_PREFIX %{CmsRelocationDir}" > %instroot/common/apt-site-env.csh

%post
find $RPM_INSTALL_PREFIX/common -name "*" -type f | xargs perl -p -i -e "s|$RPM_INSTALL_PREFIX|%{CmsRelocationDir}|g"
find $RPM_INSTALL_PREFIX/bin    -name "*" -type f | xargs perl -p -i -e "s|$RPM_INSTALL_PREFIX|%{CmsRelocationDir}|g"
find $RPM_INSTALL_PREFIX -maxdepth 1 -name "cmsset_default.*" -type f  | xargs perl -p -i -e "s|$RPM_INSTALL_PREFIX|%{CmsRelocationDir}|g"
for dir in `find $RPM_INSTALL_PREFIX/%{cmsplatf}/external/apt -maxdepth 1 -type d | grep $RPM_INSTALL_PREFIX/%{cmsplatf}/external/apt/` ; do
  if [ -d $dir/etc/profile.d ] ; then
    for ext in csh sh ; do
      ok=`grep " $RPM_INSTALL_PREFIX/common/apt-site-env.$ext " $dir/etc/profile.d/init.$ext`
      if [ "X$ok" == "X" ] ; then
        case $ext in
          csh ) echo "if ( -f $RPM_INSTALL_PREFIX/common/apt-site-env.$ext ) source  $RPM_INSTALL_PREFIX/common/apt-site-env.$ext;  endif" >> $dir/etc/profile.d/init.$ext ;;
          sh  ) echo "if [ -f $RPM_INSTALL_PREFIX/common/apt-site-env.$ext ]; then . $RPM_INSTALL_PREFIX/common/apt-site-env.$ext;  fi"    >> $dir/etc/profile.d/init.$ext ;;
        esac
      fi
    done
  fi
done

%files
%dir %{installroot}/
%dir %{installroot}/%{cmsplatf}/
%dir %{installroot}/%{cmsplatf}/%{pkgcategory}/
%dir %{installroot}/%{cmsplatf}/%{pkgcategory}/%{pkgname}/
%dir %{installroot}/%{cmsplatf}/%{pkgcategory}/%{pkgname}/%{pkgversion}/
%installroot/common/apt-site-env.sh
%installroot/common/apt-site-env.csh
