%define rpm_version %(rpm --version | grep RPM | sed 's|.* ||')
### RPM external rpm %{rpm_version}
## NOCOMPILER
## NO_AUTO_DEPENDENCY
## INITENV SET CMSPKG_SYSTEM_RPM 1

AutoReqProv: no

%prep

%build

%install
mkdir %{i}/bin
pushd %{i}/bin
cat <<EOF > rpm
#!/bin/bash
cmd=\$(basename \$0)
REALRPM="/usr/bin"
for p in /usr/bin /usr/sbin /bin; do
  if [[ -x "\$p/\$cmd" ]]; then
    REALRPM="\$p"
    break
  fi
done
\$REALRPM/\$cmd --dbpath %{cmsroot}/%{cmsplatf}/var/lib/rpm "\$@"
EOF
chmod +x rpm
ln -s rpm rpmdb
popd

%post
%{relocateConfig}bin/rpm
