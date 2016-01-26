### RPM external starlight r193
Requires: clhep

%define branch cms/%{realversion}
%define github_user cms-externals
%define tag 7d6a1b4452e576835f24a8fcf5cf9d5ce73b5528
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires:	cmake doxygen

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

export CLHEP_PARAM_PATH=${CLHEP_ROOT}

cmake ../%{n}-%{realversion} \
 -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
 -DCMAKE_BUILD_TYPE=Realease \
 -DENABLE_CLHEP=ON

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

rm -rf %{i}/lib/archive
rm -rf %{i}/lib/libStarlib.a
