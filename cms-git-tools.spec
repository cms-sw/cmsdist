### RPM cms cms-git-tools 1.0
## REVISION 1005
## NOCOMPILER

%define commit v0.6.2
%define branch master
Source0: git://github.com/cms-sw/cms-git-tools.git?obj=%{branch}/%{commit}&export=cms-git-tools&output=/cms-git-tools.tgz

%prep
#Make sure that we always build cms-common with a different revision and 
#hardcoded version 1.0 because this is what bootstrap.sh is going to install
%if "%{v}" != "1.0"
  echo "ERROR: Please do not change the version. We have to build this RPM with a different REVISION"
  echo "       Please update the revision in %n.spec and make sure that version is set to 1.0"
  exit 1
%endif

%setup -n %{n}

mkdir -p %{i}/%{pkgrevision}/common
cp * %{i}/%{pkgrevision}/common
find %{i} -name '*' -type f -exec chmod +x {} \;

%build

%install

# NOP

%post
cd ${RPM_INSTALL_PREFIX}/%{pkgrel}/%{pkgrevision}
%{relocateCmsFiles} $(find . -name '*' -type f)

mkdir -p ${RPM_INSTALL_PREFIX}/common ${RPM_INSTALL_PREFIX}/bin ${RPM_INSTALL_PREFIX}/etc/%{pkgname} ${RPM_INSTALL_PREFIX}/%{cmsplatf}/etc/profile.d

#Check if a newer revision is already installed
if [ -f ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/revision ] ; then
  oldrev=$(cat ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/revision)
  if [ ${oldrev} -ge %{pkgrevision} ] ; then
    exit 0
  fi
fi

for file in $(find . -name '*' -type f) ; do
  cp -f ${file} ${RPM_INSTALL_PREFIX}/${file}
done

echo %{pkgrevision} > ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/revision
