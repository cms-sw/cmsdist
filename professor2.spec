### RPM external professor2 2.3.2
## INITENV +PATH PYTHON3PATH %i/lib/python`echo $PYTHON3_VERSION | cut -d. -f 1,2`/site-packages

Source: http://www.hepforge.org/archive/professor/Professor-%{realversion}.tar.gz
Requires: py3-numpy py3-matplotlib root yoda eigen
BuildRequires: py3-cython

Patch0: professor2-ppc64-flag-change
Patch1: professor2_py39

%prep
%setup -n Professor-%{realversion}

%ifarch ppc64le
%patch0 -p1
%endif
%patch1 -p1

%build
make %{makeprocesses} CPPFLAGS=-I${EIGEN_ROOT}/include/eigen3 PYTHON=$(which python3) CYTHON=$(which cython3)

%install
make install PREFIX=%{i}

perl -p -i -e "s|^#!.*python.*|#!/usr/bin/env python3|" %{i}/bin/*

