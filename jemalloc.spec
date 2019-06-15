### RPM external jemalloc 5.2.0

%define tag %{realversion}
%define branch master
%define github_user jemalloc
Source: git+https://github.com/%{github_user}/jemalloc.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build
XOPTS=""
case %{cmsplatf} in
  # set the page size to 64k on ARMv8 and PowerPC
  *_aarch64_*|*_ppc64le_*|*_ppc64_*) XOPTS="--with-lg-page=16" ;;
esac

./autogen.sh ${XOPTS} \
  --enable-shared \
  --disable-static \
  --disable-doc \
  --enable-stats \
  --prefix %{i}

%post
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
