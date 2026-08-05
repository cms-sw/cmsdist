### RPM external libmnl 1.0.5
Source: https://netfilter.org/projects/libmnl/files/libmnl-%{realversion}.tar.bz2
BuildRequires: gmake
%define keep_pkgconfig true

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix=%{i} --disable-static
make %{makeprocesses}

%install
make install

%post
%relocateConfigAll lib/pkgconfig *.pc
