## INCLUDE oneapi-config
### RPM external cern-oneapi %{oneapi_version}
## INITENV SET CERN_ONEAPI_CVMFS_VERSION %{realversion}
## NOCOMPILER
%define skip_license_checks 1
%define oneapi_install_dir /cvmfs/projects.cern.ch/intelsw/oneAPI/linux/x86_64/%{oneapi_release_year}
Source: none

%prep
%build
%install 
%post
for comp in compiler vtune ; do
  if [ ! -e "%{oneapi_install_dir}/${comp}/%{realversion}" ] ; then
    >&2 echo "Error: No such file or directory: %{oneapi_install_dir}/${comp}/%{realversion}"
  fi
  ln -s "%{oneapi_install_dir}/${comp}/%{realversion}" "$RPM_INSTALL_PREFIX/%{pkgrel}/${comp}" || true
done
