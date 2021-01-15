################################################################
####For any change, always update version number to latest date#
################################################################
### RPM cms cmssw-wm-tools 210111
## NOCOMPILER
## NO_VERSION_SUFFIX

%define commit 75e66462b5b7d361816129180e7d5a38585cde35
%define branch master
Source0: git://github.com/cms-sw/%{n}.git?obj=%{branch}/%{commit}&export=%{n}&output=/%{n}-%{commit}.tgz

%prep
%if "%{v}" != "%{realversion}"
  echo "ERROR: %{v} does not match %{realversion}. Please update version number for %{n}."
  exit 1
%endif
%setup -n %{n}

%build

%install
rsync -a ./ %{i}/

%post
#Check if a newer revision is already installed
if [ -f ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version ] ; then
  if [ $(cat ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version) -ge %{realversion} ] ; then
    exit 0
  fi
fi

mkdir -p $RPM_INSTALL_PREFIX/share/overrides ${RPM_INSTALL_PREFIX}/etc/%{pkgname}
for d in bin python ; do
  rsync -a ${RPM_INSTALL_PREFIX}/%{pkgrel}/$d/ $RPM_INSTALL_PREFIX/share/overrides/$d/
done
echo %{realversion} > ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version
