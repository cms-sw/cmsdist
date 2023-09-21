### RPM external pacparser 1.4.2
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
Source: https://github.com/manugarg/pacparser/archive/refs/tags/v%{realversion}.tar.gz
Requires: python3
BuildRequires: py3-setuptools

%prep
%setup -n %{n}-%{realversion}

%build
make -C src all pymod PREFIX=%{i} PYTHON=$(which python3)

%install
make -C src install install-pymod \
  PREFIX=%{i} \
  PYTHON=$(which python3) \
  PYTHONUSERBASE=%{i} \
  EXTRA_ARGS="--user"

find %{i}/lib -type f | xargs chmod 0755

%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}
