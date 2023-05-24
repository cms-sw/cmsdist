## INCLUDE cuda-version
### RPM external cuda %{cuda_version}

%install
mkdir -p %i
for item in $(ls -d %{cuda_install_dir}/*) ; do
  ln -s $item %{i}/
done
