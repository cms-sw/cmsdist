### RPM external professor2 2.4.2
## INITENV +PATH PYTHON3PATH %i/lib/python%{cms_python3_major_minor_version}/site-packages
## INCLUDE cpp-standard

Source: git+https://gitlab.com/hepcedar/professor.git?obj=main/professor-%{realversion}&export=professor-%{realversion}&output=/professor-%{realversion}.tgz
Requires: py3-matplotlib root yoda eigen py3-iminuit
BuildRequires: py3-cython py3-pip

Patch0: professor2-ppc64-flag-change

%prep
%setup -n professor-%{realversion}

%ifarch ppc64le
%patch0 -p1
%endif
%ifarch riscv64
sed -i -e 's|-march=native||' Makefile
%endif

# Make sure the default c++sdt stand is c++11 in pyext/setup.py
grep -q 'std=c[+][+]11' pyext/setup.py
# Change c++ std to 17
sed -i -e 's|-std=c[+][+]11|-std=c++%{cms_cxx_standard}|' pyext/setup.py
# Same for Makefile
grep -q 'CXXSTD := c[+][+]11' Makefile
sed -i -e 's|CXXSTD := c[+][+]11|CXXSTD := c++%{cms_cxx_standard}|' Makefile
sed -i -e "s|pip install -vv|pip install --target ../${PYTHON3_LIB_SITE_PACKAGES} -vv|" Makefile

# Update Python2 to Python3
for i in `ls bin`
do
   echo "bin/${i}"
   sed -i -e 's|/usr/bin/env python|/usr/bin/env python3|' "bin/${i}"
done

%define build_flags CPPFLAGS=-I${EIGEN_ROOT}/include/eigen3 PYTHON=$(which python3) PROF_VERSION=%{realversion} PYTHONPATH=./${PYTHON3_LIB_SITE_PACKAGES}:./pyext/professor2

%build
make PREFIX=%{i} %{build_flags}

%install
make install PREFIX=%{i} %{build_flags}
mv %{i}/${PYTHON3_LIB_SITE_PACKAGES}/%{n}-%{realversion}*.dist* %{i}/${PYTHON3_LIB_SITE_PACKAGES}/%{n}
rm -f %{i}/${PYTHON3_LIB_SITE_PACKAGES}/*.pth


