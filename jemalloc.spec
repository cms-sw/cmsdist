### RPM external jemalloc 4.5.99

%define tag 31baedbbb9d1701b13312415b59d2b6240bb18e4
%define branch dev
%define github_user jemalloc
Source: git+https://github.com/%{github_user}/jemalloc.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build
# Disable documentation (not needed)
sed -ibak 's/install: install_bin install_include install_lib install_doc/install: install_bin install_include install_lib/' Makefile.in
./autogen.sh

./configure \
  --disable-stats \
  --prefix %{i}

%post
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
