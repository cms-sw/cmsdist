### RPM external giflib 4.2.3
Source: http://heanet.dl.sourceforge.net/project/%{n}/%{n}-4.x/%{n}-%{realversion}.tar.bz2

BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build
# We do not have xmlto, thus disable documentation
sed -ibak '1s/doc//' Makefile.am
autoreconf -fiv

./configure --prefix=%{i}

make %{makeprocesses}

%install
make install

%define strip_files %{i}/lib
