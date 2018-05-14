### RPM external jemalloc 5.0.1

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
  *_aarch64_*|*_ppc64le_*|*_ppc64_*) XOPTS="--with-lg-page=16" ;;
esac

# Disable documentation (not needed)
sed -ibak 's/install: install_bin install_include install_lib install_doc/install: install_bin install_include install_lib/' Makefile.in
./autogen.sh

./configure ${XOPTS}\
  --enable-stats \
  --enable-prof \
  --prefix %{i}

%post
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
