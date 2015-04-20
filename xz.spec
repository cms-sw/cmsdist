### RPM external xz 5.2.1__5.1.2alpha
%define generic_version 5.2.1
%define fcarm_version 5.1.2alpha
%define tag dec11497a71518423b5ff0e759100cf8aadf6c7b
%define branch cms/v%generic_version
%define github_user degano
%define armtag 5cc6656
%define armbranch cms/v%fcarm_version
%define isfcarm %(case %{cmsplatf} in (fc*_arm*) echo 1 ;; (*) echo 0 ;; esac)
#Source0: git+https://github.com/%github_user/xz.git?obj=%{branch}/%{tag}&export=%{n}-%{generic_version}&output=/%{n}-%{generic_version}.tgz
Source0: http://tukaani.org/xz/xz-%{generic_version}.tar.gz
Source1: git+https://github.com/%github_user/xz.git?obj=%{armbranch}/%{armtag}&export=%{n}-%{fcarm_version}&output=/%{n}-%{fcarm_version}.tgz

BuildRequires: autotools

%prep
%if %isfcarm
%setup -b 1 -n %{n}-%{fcarm_version}
%else
%setup -b 0 -n %{n}-%{generic_version}
%endif

%build
./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static --disable-nls --disable-rpath --disable-dependency-tracking --disable-doc
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
