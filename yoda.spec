### RPM external yoda 1.8.0
## INITENV +PATH PYTHON27PATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}

Source: git+https://gitlab.com/hepcedar/yoda.git?obj=master/%{n}-%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Patch0: yoda_pyroot

Requires: python python3 root
BuildRequires: py2-cython autotools

%prep
%setup -q -n %{n}-%{realversion}
%patch0 -p1

autoreconf -fiv

%build

sed -i -e "s|lPyROOT|lcppyyX.X|" ./pyext/setup.py.in

#Build for Python3
export PYTHON_VERSION=$(python3 --version 2>&1 | sed 's|.* ||' | cut -d. -f1,2)
sed -i -e "s|lcppyy...|lcppyy$(echo ${PYTHON_VERSION} | tr . _)|" ./pyext/setup.py.in
./configure --prefix=%i --enable-root
make %{makeprocesses} all

#Install Py3 Only
mkdir -p %{i}/${PYTHON3_LIB_SITE_PACKAGES}
mv pyext/build/lib*-${PYTHON_VERSION}/yoda* %{i}/${PYTHON3_LIB_SITE_PACKAGES}/

#Build & install for Python2
export PYTHON_VERSION=$(python2 --version 2>&1 | sed 's|.* ||' | cut -d. -f1,2)
sed -i -e "s|lcppyy...|lcppyy$(echo ${PYTHON_VERSION} | tr . _)|" ./pyext/setup.py.in
./configure --prefix=%i --enable-root
make %{makeprocesses} all
make install

%install

%post
%{relocateConfig}bin/yoda-config
