### RPM external jemalloc-debug 4.5.0

%define tag %{realversion}
%define branch master
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
  --enable-stats \
  --prefix %{i} \
  --enable-debug \
  --enable-fill

%post
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
# bla bla
