### RPM external nasm 2.11.02
Source: http://www.nasm.us/pub/nasm/releasebuilds/%{realversion}/%{n}-%{realversion}.tar.bz2

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix=%{i}

make %{makeprocesses}
%install
make install

%define drop_files %{i}/share
# bla bla
