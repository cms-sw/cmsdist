### RPM external xz 5.2.4

%define tag b5be61cc06088bb07f488f9baf7d447ff47b37c1
%define branch cms/v%{realversion}
%define github_user cms-externals
Source0: git+https://github.com/%github_user/xz.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build
./autogen.sh
./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static --disable-nls --disable-rpath --disable-dependency-tracking --disable-doc
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
