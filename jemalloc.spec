### RPM external jemalloc 5.2.1

%define tag de1caefb587217f0b519eb425d7a9b3570e5ba28
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/jemalloc.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build

./autogen.sh --enable-shared \
  --disable-static \
  --disable-doc \
  --enable-stats \
  --prefix %{i}

%post
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
