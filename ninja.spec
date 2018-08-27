### RPM external ninja 1.8.2
Source0: git://github.com/ninja-build/ninja.git?obj=release/v%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: python re2c

%prep
%setup -T -b 0 -n %{n}-%{realversion}

%build
./bootstrap.py

%install
mkdir -p %{i}/bin
cp ninja %{i}/bin
