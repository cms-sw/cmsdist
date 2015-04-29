### RPM external xz 5.2.1

%define tag 14937fff889113f477d6f60098186f932e72c0e4
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
