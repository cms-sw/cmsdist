### RPM external pandora 0.1_cms1

%define tag e4825cb52f9a6c8b04ec93b9506b12631e3a475f
%define branch master
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: cmake

%define pan_dir %_builddir/%{n}-%{realversion}

%prep
%setup -q -n %{n}-%{realversion}
mkdir -p %pan_dir/lib
%build
export PANDORA_DIR=%pan_dir
make

%install
cp -r %pan_dir/lib %{i}/
mkdir -p %{i}/include/PandoraSDK
mkdir -p %{i}/include/LCContent
cp -r %pan_dir/PandoraSDK/include %{i}/include/PandoraSDK
cp -r %pan_dir/LCContent/include %{i}/include/LCContent
