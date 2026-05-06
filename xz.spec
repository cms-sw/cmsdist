### RPM external xz 5.8.3
Source0: http://tukaani.org/xz/xz-%{realversion}.tar.gz

BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build
./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static --disable-nls --disable-rpath --disable-dependency-tracking --disable-doc
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
