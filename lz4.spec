### RPM external lz4 1.8.2

%define tag %{realversion}
%define branch tbb_2018
%define github_user lz4
Source: https://github.com/%{github_user}/lz4/archive/v%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build

make %{makeprocesses} 

%install


make DESTDIR=%i install

# bla bla
