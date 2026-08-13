### RPM external nasm 3.01
Source: https://www.nasm.us/pub/nasm/releasebuilds/%{realversion}/%{n}-%{realversion}.tar.gz
BuildRequires: gmake

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix=%{i}

make %{makeprocesses}
%install
make install

%define drop_files %{i}/share
