### RPM external xz 5.0.3__5.1.2alpha
%define generic_version 5.0.3
%define fcarm_version 5.1.2alpha
%define tag 931d2d5
%define branch cms/v%generic_version
%define github_user cms-externals
%define armtag 5cc6656
%define armbranch cms/v%fcarm_version
Source0: git+https://github.com/%github_user/xz.git?obj=%{branch}/%{tag}&export=%{n}-%{generic_version}&output=/%{n}-%{generic_version}.tgz
Source1: git+https://github.com/%github_user/xz.git?obj=%{armbranch}/%{armtag}&export=%{n}-%{fcarm_version}&output=/%{n}-%{fcarm_version}.tgz

%prep
%if %isfcarm
%setup -b 1 -n %{n}-%{fcarm_version}
%else
%setup -b 0 -n %{n}-%{generic_version}
%endif

%build
./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
