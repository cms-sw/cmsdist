### RPM external jemalloc 5.2.1

%define tag 8b5961b8a2ce67f1182f13ed5ce1adad3e2e99c1
%define branch cms/%{realversion}
%define github_user cms-externals
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
