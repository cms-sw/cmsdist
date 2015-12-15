### RPM external ninja 1.6.0
Source0: git://github.com/martine/ninja.git?obj=release/v%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: python re2c

%prep
%setup -T -b 0 -n %{n}-%{realversion}

%build
./bootstrap.py

%install
mkdir -p %{i}/bin
cp ninja %{i}/bin
