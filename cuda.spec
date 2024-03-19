Requires: cuda-runtime
## INCLUDE cuda-version
### RPM external cuda %{cuda_version}

%install
mkdir -p %i
for item in $(ls -d %{cuda_install_dir}/*) ; do
  dir=$(basename $item)
  if [ $dir != "etc" ] ; then
    ln -s $item %{i}/
  else
    mkdir %{i}/etc
    for sitem in $(ls -d %{cuda_install_dir}/etc/*) ; do
      ln -s $sitem %{i}/etc/
    done
  fi
done
