### RPM external xz 5.2.5

%define tag 50f585dc3b7b9b94b6b7f7a4c29903602d1e2a2d
%define branch cms/v%{realversion}
%define github_user cms-externals
Source0: git+https://github.com/%github_user/xz.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build
./autogen.sh --no-po4a
./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static --disable-nls --disable-rpath --disable-dependency-tracking --disable-doc
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
