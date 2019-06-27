### RPM external giflib 5.2.0

Source: https://sourceforge.net/projects/giflib/files/giflib-%{realversion}.tar.gz
BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build

# "fix" the doc makefile
echo "all:" > doc/Makefile
make all %{makeprocesses}

%install
make PREFIX=%{i} install-bin
make PREFIX=%{i} install-include
make LIBVER=%{realversion} LIBMAJOR=5 PREFIX=%{i} install

%define strip_files %{i}/lib
