### RPM external md5 2.0.0
%define tag 1ed14d187d793216fb8345363f590bf3effd95e2
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

%ifarch darwin
c++ edm_md5.c -shared -fPIC -o libcms-md5.dylib
%else
c++ edm_md5.c -shared -fPIC -o libcms-md5.so
%endif

%install

mkdir %{i}/{lib,include}
cp libcms-md5.* %{i}/lib/
cp edm_md5.h %{i}/include/
