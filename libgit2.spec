### RPM external libgit2 0.27.3

Source0: https://github.com/%{n}/%{n}/archive/v%{realversion}.tar.gz

Requires: python
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}

%build
mkdir cmake-build
cd cmake-build
cmake -DCMAKE_RELEASE_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{i} ..
make

%install
cd cmake-build
make install
