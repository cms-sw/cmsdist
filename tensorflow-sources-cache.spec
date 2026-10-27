## INCLUDE tensorflow/version
### RPM external tensorflow-sources-cache %{tf_version}
%define tf_external_source_version cp314
%define fetch_externals yes
%define fetch_externals_file tensorflow-%{realversion}.txt

%define fetch_cached_sources()                                     \
  for item in $(cat %{2}) ; do                                     \
    path=$(echo $item | sed 's|^[0-9a-f]*:[0-9a-f]*:||')           \
    if [ ! -e %{1}/${path} ] ; then                                \
      md5=$(echo $item | cut -d: -f1)                              \
      ch2=$(echo ${md5} | cut -c1-2)                               \
      fmd5=$(echo $item | cut -d: -f2)                             \
      sha_dir=$(dirname $path)                                     \
      mkdir -p %{1}/${sha_dir}                                     \
      urls=""                                                      \
      for mirror in %{source_mirrors} ; do                         \
        urls="${urls} ${mirror}/SOURCES/cache/${ch2}/${md5}/${md5}"\
      done                                                         \
      for repo in %{package_repository} ; do                       \
        urls="$urls %{repository_server}/SOURCES/${repo}/${md5}/${md5}" \
      done                                                         \
      for url in ${urls} ; do                                      \
        if curl -fL -k -s -o %{1}/${path}.tmp "${url}" ; then      \
          if [ "$(md5sum %{1}/${path}.tmp | cut -d' ' -f1)" = "$fmd5" ] ; then \
            mv %{1}/${path}.tmp %{1}/${path}                       \
            break                                                  \
          fi                                                       \
        fi                                                         \
        rm -f %{1}/${path}.tmp                                     \
      done                                                         \
    fi                                                             \
  done

%define fetch_bazel_sources                                      \
  if [ -e "%{SOURCE99}" ] ; then                                 \
    %fetch_cached_sources %{cmsroot} %{SOURCE99}                 \
  fi                                                             \
  bazel $(echo "$BAZEL_OPTS" | sed -e 's| build | fetch |') //tensorflow/tools/pip_package:wheel \
  rm -f %{_builddir}/%{fetch_externals_file}                             \
  touch %{_builddir}/%{fetch_externals_file}                             \
  for f in $(find %{repo_cache} -name '*' -type f | sed 's|^%{cmsroot}/||' | sort) ; do \
    md5=$(echo -n $f | md5sum | cut -d' ' -f1)                           \
    fmd5=$(md5sum %{cmsroot}/$f | cut -d' ' -f1)                         \
    echo "${md5}:${fmd5}:${f}" >> %{_builddir}/%{fetch_externals_file}   \
  done                                                                   \
  if [ -e "%{SOURCE99}" ] ; then                                         \
    if ! diff -u %{SOURCE99} %{_builddir}/%{fetch_externals_file} ; then \
      echo "ERROR: Bazel fetch sources changes w.r.t previous download"  \
      echo "       Try to understand this change and udd/pdate version"  \
      echo "       in tf_external_source_version RPM spec micro."        \
      exit 1                                                             \
    fi                                                                   \
  fi

%define prepare_upload_sources                                               \
  if [ ! -e "%{SOURCE99}" ] ; then                                           \
    chksum_source="SOURCES/cache/$(echo %{cmsdist_chksum_source99} | cut -c1-2)/%{cmsdist_chksum_source99}" \
    mkdir -p %{cmsroot}/${chksum_source}                                     \
    cp %{_builddir}/%{fetch_externals_file} %{cmsroot}/${chksum_source}/     \
    ln -s %{cmsroot}/${chksum_source}/%{fetch_externals_file} %{SOURCE99}    \
    for item in $(cat %{SOURCE99}) ; do                                      \
      md5=$(echo $item | cut -d: -f1)                                        \
      path=$(echo $item | sed 's|^[0-9a-f]*:[0-9a-f]*:||')                   \
      dir="SOURCES/cache/$(echo ${md5} | cut -c1-2)/${md5}"                  \
      mkdir -p %{cmsroot}/${dir}                                             \
      cp %{cmsroot}/${path} %{cmsroot}/${dir}/${md5}                         \
    done                                                                     \
  fi                                                                         \
  mkdir -p %{i}                                                              \
  cp -L %{SOURCE99} %{i}/

## INCLUDE tensorflow/build
