%define hipblaslt_enable_device ON
## INITENV SET HIPBLASLT_TENSILE_LIBPATH %{i}/tensile
## INCLUDE rocm/hipblaslt-common
### RPM external hipblaslt-tensile %{rocm_version_num}

%define rocm_project hipblaslt
%{expand:%(i=80; for t in $(echo "%{rocm_targets}" | tr ';' ' '); do echo "Source${i}: https://cmsrep.cern.ch/cmssw/download/%{rocm_project}/%{rocm_version_num}/%{_arch}?cmsdist-generated=1&v=1&output=/tensile-${t}.tar.gz"; i=$((i+1)); done)}
BuildRequires: py3-joblib py3-msgpack py3-packaging py3-PyYAML

%define set_gpu_archs \
  GPU_ARCHS=$(cat %{_builddir}/gpu-archs.txt) \
  if [ "${GPU_ARCHS}" == "" ] ; then \
    ROCM_SKIP_BUILD=true \
  fi

%define ROCMPreCMakeRun \
  %{set_gpu_archs} \
  if [ "${GPU_ARCHS}" != "" ] ; then CMAKE_ARGS+=("-DGPU_TARGETS=${GPU_ARCHS}") ; fi

%define ROCMPreInstall %{set_gpu_archs}

%define ROCMPostInstall \
  for t in $(echo "${GPU_ARCHS}" |  tr ';' ' '); do \
    line=$(grep "^${t}:" %{_builddir}/gpu-sources.txt) \
    o=$(echo "$line" | cut -d: -f3 | sed 's|.*/||') \
    s=$(echo "$line" | cut -d: -f2) \
    tar -C %{i}/lib64/hipblaslt/library -czf %{_builddir}/${o} ${t} \
    %copy_source_to_cache ${o} $s \
  done \
  rm -rf %{i} \
  mkdir -p %{i}/hipblaslt/library %{i}/tensile \
  for line in $(cat %{_builddir}/gpu-sources.txt ); do \
    t=$(echo "$line" | cut -d: -f1) \
    o=$(echo "$line" | cut -d: -f3) \
    tar -C %{i}/hipblaslt/library -xzf ${o} \
    for file in "%{i}/hipblaslt/library/$t"/*; do \
      [ -f "$file" ] || continue \
      name=${file##*/} \
      ln -sfn "../hipblaslt/library/${t}/$name" "%{i}/tensile/${name}" \
    done \
  done

%define ROCMPrePrep \
  rm -f %{_builddir}/gpu-sources.txt \
  touch %{_builddir}/gpu-sources.txt \
  %{expand:%(i=80; for t in $(echo "%{rocm_targets}" | tr ';' ' '); do echo "echo $t:%%{cmsdist_chksum_source$i}:%%{SOURCE$i} >> %{_builddir}/gpu-sources.txt"; i=$((i+1)); done)} \
  GPU_ARCHS="" \
  for line in $(cat %{_builddir}/gpu-sources.txt ); do \
    o=$(echo "$line" | cut -d: -f3) \
    [ -e "$o" ] && continue \
    t=$(echo "$line" | cut -d: -f1) \
    GPU_ARCHS="${GPU_ARCHS:+${GPU_ARCHS};}${t}" \
  done \
  echo "${GPU_ARCHS}" > %{_builddir}/gpu-archs.txt

## INCLUDE rocm/libraries-build
