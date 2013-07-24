### RPM cms cms-git-tools 6.0
## NOCOMPILER

# ***Do not change minor number of the above version.***

%define commit v0.11.0
%define branch master
# We do not use a revision explicitly, because revisioned packages do not get
# updated automatically when they are dependencies.
%define fakerevision %(echo %realversion | cut -d. -f1)
Source0: git://github.com/cms-sw/cms-git-tools.git?obj=%{branch}/%{commit}&export=cms-git-tools&output=/cms-git-tools.tgz

%prep
%setup -n %{n}

mkdir -p %{i}/common %{i}/share/man/man1
cp git-cms-* %{i}/common
cp docs/man/man1/*.1 %{i}/share/man/man1
find %{i}/common -name '*' -type f -exec chmod +x {} \;

%build

%install

# NOP

%post
cd ${RPM_INSTALL_PREFIX}/%{pkgrel}
%{relocateCmsFiles} $(find . -name '*' -type f)

mkdir -p ${RPM_INSTALL_PREFIX}/common ${RPM_INSTALL_PREFIX}/etc/%{pkgname} ${RPM_INSTALL_PREFIX}/share/man/man1

#Check if a newer revision is already installed
if [ -f ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version ] ; then
  oldrev=$(cat ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version )
  if [ ${oldrev} -ge %{fakerevision} ] ; then
    exit 0
  fi
fi

for file in $(find . -name '*' -type f -path '*/common/*' -o -type f -path '*/share/*') ; do
  cp -f ${file} ${RPM_INSTALL_PREFIX}/${file}
done
rm -f ${RPM_INSTALL_PREFIX}/common/git-addpkg
rm -f ${RPM_INSTALL_PREFIX}/common/git-checkdeps

echo %{fakerevision} > ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version
