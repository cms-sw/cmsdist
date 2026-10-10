## INCLUDE tensorflow/version
### RPM external tensorflow-sources-cache %{tf_version}
 
%define fetch_externals yes
%define fetch_externals_file tensorflow-%{realversion}.txt

%define fetch_cached_sources()                                     \
  for item in $(cat %{1}/%{pkgrel}/%{fetch_externals_file}) ; do   \
    md5=$(echo $item | cut -d: -f1)                                \
    fmd5=$(echo $item | cut -d: -f2)                               \
    path=$(echo $item | sed 's|^[0-9a-f]*:[0-9a-f]*:||')           \
    if [ ! -e %{1}/${path} ] ; then                                \
      sha_dir=$(dirname $path)                                     \
      mkdir -p %{1}/${sha_dir}                                     \
      for repo in %{package_repository} ; do                       \
        if curl -fL -k -s -o %{1}/${path}.tmp "http://cmsrep.cern.ch/cgi-bin/cmspkg/SOURCES/${repo}/${md5}/${md5}" ; then \
          if [ "$(md5sum %{1}/${path}.tmp | cut -d' ' -f1)" = "$fmd5" ] ; then \
            mv %{1}/${path}.tmp %{1}/${path}                       \
            break                                                  \
          fi                                                       \
        fi                                                         \
        rm -f %{1}/${path}.tmp                                     \
      done                                                         \
    fi                                                             \
  done

%define fetch_bazel_sources                                        \
  if [ ! -e "%{SOURCE99}" ] ; then                                 \
    bazel $(echo "$BAZEL_OPTS" | sed -e 's| build | fetch |') //tensorflow/tools/pip_package:wheel \
    rm -f %{_builddir}/%{fetch_externals_file}                     \
    touch %{_builddir}/%{fetch_externals_file}                     \
    for f in $(find %{repo_cache} -name '*' -type f | sed 's|^%{cmsroot}/||' | sort) ; do \
      md5=$(echo -n $f | md5sum | cut -d' ' -f1)                           \
      fmd5=$(md5sum %{cmsroot}/$f | cut -d' ' -f1)                         \
      echo "${md5}:${fmd5}:${f}" >> %{_builddir}/%{fetch_externals_file}   \
    done                                                                   \
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
