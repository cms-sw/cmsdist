### RPM cms cms-common 1.0
## REVISION 1226
## NOCOMPILER

%define tag 9c6c3803c5d21f1b5da88eceb4f76f0145c163e1
Source:  git+https://github.com/cms-sw/cms-common.git?obj=master/%{tag}&export=%{n}-%{realversion}-%{tag}&output=/%{n}-%{realversion}-%{tag}.tgz

%prep
#Make sure that we always build cms-common with a different revision and 
#hardcoded version 1.0 because this is what bootstrap.sh is going to install
%if "%{v}" != "1.0"
  echo "ERROR: Please do not change the version. We have to build this RPM with a different REVISION"
  echo "       Please update the revision in %{n}.spec and make sure that version is set to 1.0"
  exit 1
%endif
%setup -n %{n}-%{realversion}-%{tag}
find . -type f | xargs sed -i -e 's|@CMS_PREFIX@|%{instroot}|g;s|@SCRAM_ARCH@|%{cmsplatf}|'

%build

%install
mkdir -p %{i}/%{pkgrevision}
rsync -a %_builddir/%{n}-%{realversion}-%{tag}/ %{i}/%{pkgrevision}/

%post
cd $RPM_INSTALL_PREFIX/%{pkgrel}/%{pkgrevision}
%{relocateCmsFiles} `find . -name "*" -type f`

mkdir -p $RPM_INSTALL_PREFIX/etc/%{pkgname}  $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/profile.d

#Check if a newer revision is already installed
#Also force installation if older revision has deleted cmsset_default.sh
if [ -f $RPM_INSTALL_PREFIX/cmsset_default.csh ] && [ -f $RPM_INSTALL_PREFIX/etc/%{pkgname}/revision ] ; then
  oldrev=`cat $RPM_INSTALL_PREFIX/etc/%{pkgname}/revision`
  if [ $oldrev -ge %{pkgrevision} ] ; then
    exit 0
  fi
fi

for file in $(find . -name '*'); do
  if [ -d $file ] ; then
    mkdir -p $RPM_INSTALL_PREFIX/$file
  else
    rm -f $RPM_INSTALL_PREFIX/$file
    cp -P $file $RPM_INSTALL_PREFIX/$file
  fi
done
echo %{pkgrevision} > $RPM_INSTALL_PREFIX/etc/%{pkgname}/revision
