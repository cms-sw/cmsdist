### RPM external ninja 1.11.1
Source0: git://github.com/ninja-build/ninja.git?obj=release/v%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: python3 re2c

%prep
%setup -T -b 0 -n %{n}-%{realversion}

%build
python3 ./configure.py --bootstrap

%install
mkdir -p %{i}/bin
cp ninja %{i}/bin
