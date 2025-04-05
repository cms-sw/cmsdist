### RPM external rocm-rocrand 6.3.4
## NOCOMPILER

%if 0%{?rhel} == 7
# allow rpm2cpio dependency on the bootstrap bundle
%undefine drop_bootstrap_lib
%define drop_bootstrap_lib true
%define repository repo.radeon.com/rocm/yum
%else
%define repository repo.radeon.com/rocm/rhel%{rhel}
%endif

# AMD repositories are numbered 6.2, 6.2.1, 6.2.2, ..., 6.3
# without any .0 in the directory name
%define repoversion %(echo %{realversion} | sed -e's/\.0$//')
%define baseurl %{repository}/%{repoversion}/main/
%define rpm_version '[0-9]\+\(\.[0-9]\+\)*-[0-9]\+\(\.el%{rhel}\)\?\.%{_arch}'
%define packages            \\\
  rocrand                   \\\
  rocrand-devel

# generate the Source statements for the list of packages
%{expand:%(curl -s %{baseurl} |
  sed -n -e's#<a href="\([^"]*.rpm\)".*#\1#p' |
  grep -v -e '-asan' |
  grep -v -e '-debug' |
  grep -v -e '-rpath' |
  grep -v -F '%{realversion} -' |
  grep "$(for P in %{packages}; do echo -n ^$P-%{rpm_version}.rpm'\|'; done; echo 'do_not_match')" |
  sort |
  awk '{ printf "Source%d: %s/%s\n", NR-1, "'${baseurl}'", $0; }')}

Requires: rocm
AutoReq: no

%prep

%build
# generate the build statements from the list of packages
%{expand:%(for P in %{packages}; do echo $P; done | awk '{ printf "rpm2cpio %{SOURCE%d} | cpio -idmv\n", NR-1 }')}

%install
rmdir %{i}
mv opt/rocm-%{realversion} %{i}
rm -rf opt
rm -rf usr

%post
