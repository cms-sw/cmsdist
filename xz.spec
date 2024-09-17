### RPM external xz 5.6.2
Source: https://github.com/tukaani-project/xz/archive/refs/tags/v%{realversion}.tar.gz
BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build
./autogen.sh --no-po4a
./configure CFLAGS='-fPIC -Ofast -fno-fast-math' --prefix=%{i} --disable-static --disable-nls --disable-rpath --disable-dependency-tracking --disable-doc
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
