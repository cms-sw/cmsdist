### RPM external re2c 0.13.5
Source0: http://heanet.dl.sourceforge.net/project/%{n}/%{n}/%{realversion}/%{n}-%{realversion}.tar.gz

%prep
%setup -T -b 0 -n %{n}-%{realversion}

%build
./configure --prefix=%{i}
make %{makeprocesses}

%install
make install

# Drop not essential files
rm -rf %{i}/share
