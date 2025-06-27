### RPM cms cms-cat 250627.0
## NOCOMPILER
## NO_VERSION_SUFFIX

# ***Do not change minor number of the above version. ***

%define commit 5cf28195a12d7c98bfccdb36a5fffa7b36247af5
%define branch master
# We do not use a revision explicitly, because revisioned packages do not get
# updated automatically when there are dependencies.
%define fakerevision %(echo %realversion | cut -d. -f1)
Source0: git://gitlab.cern.ch/cms-analysis/services/cms.cern.ch-cat.git?obj=%{branch}/%{commit}&export=cms-cat&output=/cms-cat-%{commit}.tgz

%prep
%setup -n %{n}

%build

%install
mkdir -p %{i}/cat
mv * %{i}/cat

%post
cd ${RPM_INSTALL_PREFIX}/%{pkgrel}
mkdir -p ${RPM_INSTALL_PREFIX}/cat ${RPM_INSTALL_PREFIX}/etc/%{pkgname}

# Check if a newer revision is already installed
if [ -f ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version ] ; then
  oldrev=$(cat ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version )
  if [ ${oldrev} -ge %{fakerevision} ] ; then
    exit 0
  fi
fi

rsync -a --delete ${RPM_INSTALL_PREFIX}/%{pkgrel}/cat/ ${RPM_INSTALL_PREFIX}/cat/

echo %{fakerevision} > ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version
