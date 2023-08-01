### RPM external professor2 2.3.3
## INITENV +PATH PYTHON3PATH %i/lib/python%{cms_python3_major_minor_version}/site-packages

Source: http://www.hepforge.org/archive/professor/Professor-%{realversion}.tar.gz
Requires: py3-matplotlib root yoda eigen
BuildRequires: py3-cython py3-pip

Patch0: professor2-ppc64-flag-change

%prep
%setup -n Professor-%{realversion}

%ifarch ppc64le
%patch0 -p1
%endif

# Make sure the default c++sdt stand is c++11 in pyext/setup.py
grep -q 'std=c[+][+]11' pyext/setup.py
# Change c++ std to 17
sed -i -e 's|-std=c[+][+]11|-std=c++17|' pyext/setup.py
# Same for Makefile
grep -q 'CXXSTD := c[+][+]11' Makefile
sed -i -e 's|CXXSTD := c[+][+]11|CXXSTD := c++17|' Makefile

%define build_flags CPPFLAGS=-I${EIGEN_ROOT}/include/eigen3 PYTHON=$(which python3) PROF_VERSION=%{realversion} PYTHONPATH=./${PYTHON3_LIB_SITE_PACKAGES}

%build
make %{build_flags}

%install
make install PREFIX=%{i} %{build_flags}
mv %{i}/${PYTHON3_LIB_SITE_PACKAGES}/%{n}-%{realversion}*.egg %{i}/${PYTHON3_LIB_SITE_PACKAGES}/%{n}
rm -f %{i}/${PYTHON3_LIB_SITE_PACKAGES}/*.pth
