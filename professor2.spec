### RPM external professor2 2.3.2
## INITENV +PATH PYTHON3PATH %i/lib/python%{cms_python3_major_minor_version}/site-packages

Source: http://www.hepforge.org/archive/professor/Professor-%{realversion}.tar.gz
Requires: py3-matplotlib root yoda eigen
BuildRequires: py3-cython

Patch0: professor2-ppc64-flag-change

%prep
%setup -n Professor-%{realversion}

%ifarch ppc64le
%patch0 -p1
%endif

%build
make CPPFLAGS=-I${EIGEN_ROOT}/include/eigen3 PYTHON=$(which python3)

%install
make install PREFIX=%{i}

find %{i} -type f -exec sed -ideleteme '1 { s|^#!.*/bin/python.*|#!/usr/bin/env python3| }' {} \;
find %{i} -name '*deleteme' -delete
