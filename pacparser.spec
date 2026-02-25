### RPM external pacparser 1.5.0
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
Source: https://github.com/manugarg/pacparser/archive/refs/tags/v%{realversion}.tar.gz
Patch0: patches/pacparser-pymod-install
Requires: python3
BuildRequires: py3-setuptools

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
CFLAGS='-pthread' make -C src all pymod PREFIX=%{i} PYTHON=$(which python3)

%install
make -C src install install-pymod \
  PREFIX=%{i} \
  PYTHON=$(which python3) \
  EXTRA_ARGS="--prefix=%{i}"

find %{i}/lib -type f | xargs chmod 0755

%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}
