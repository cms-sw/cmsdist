### RPM external md5 1.0.0
%define tag d97a571864a119cd5408d2670d095b4410e926cc
%define branch cms/1.0.0
%define github_user cms-externals
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}.%{realversion}&output=/%{n}.%{realversion}-%{tag}.tgz

%prep
%setup -n %{n}.%{realversion}

%build

%if %isdarwin
gcc md5.c -shared -fPIC -o libcms-md5.dylib
%else
gcc md5.c -shared -fPIC -o libcms-md5.so
%endif

%install

mkdir %{i}/{lib,include}
cp libcms-md5.* %{i}/lib/
cp md5.h %{i}/include/
# bla bla
