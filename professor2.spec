### RPM external professor2 2.2.2
## INITENV +PATH PYTHON27PATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages

Source: http://www.hepforge.org/archive/professor/Professor-%{realversion}.tar.gz
Requires: py2-numpy py2-matplotlib root yoda eigen
BuildRequires: py2-cython

Patch0: professor2-ppc64-flag-change

%prep
%setup -n Professor-%{realversion}

%ifarch ppc64le
%patch0 -p1
%endif

%build
make CPPFLAGS=-I${EIGEN_ROOT}/include/eigen3

%install
make install PREFIX=%{i}

find %{i} -type f -exec sed -ideleteme '1 { s|^#!.*/bin/python|#!/usr/bin/env python| }' {} \;
find %{i} -name '*deleteme' -delete
