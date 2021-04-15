### RPM external tbb 2021.2.0

%define tag v%{realversion}
%define branch onetbb_2021
%define github_user oneapi-src
Source: git+https://github.com/%{github_user}/oneTBB.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}


%build
mkdir build
cd build
cmake .. -DCMAKE_CXX_STANDARD=17 -DCMAKE_INSTALL_PREFIX=%{i}
make %{makeprocesses}
make %{makeprocesses} install

%install
