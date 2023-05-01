### RPM external re2c 1.0.1
Source0: https://deac-ams.dl.sourceforge.net/project/%{n}/%{realversion}/%{n}-%{realversion}.tar.gz

%prep
%setup -T -b 0 -n %{n}-%{realversion}

%build
./configure --prefix=%{i}
make %{makeprocesses}

%install
make install

# Drop not essential files
rm -rf %{i}/share
