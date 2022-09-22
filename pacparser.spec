### RPM external pacparser 1.4.0
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
Source: https://github.com/%{n}/%{n}/releases/download/v%{realversion}/%{n}-v%{realversion}.tar.gz
Patch0: pacparser-python-fix
Requires: python3
BuildRequires: py3-setuptools

%prep
%setup -n %{n}-v%{realversion}
%patch0 -p1

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
