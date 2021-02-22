### RPM external tbb 2020_U3

%define tag %{realversion}
%define branch tbb_2020
%define github_user oneapi-src
Source: git+https://github.com/%{github_user}/oneTBB.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}

%build

make %{makeprocesses} stdver=c++17 tbb_cpf=1

%install
install -d %i/lib
cp -r include %i/include
case %cmsplatf in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac
find build -name "*.$SONAME*" -exec cp {} %i/lib \; 
for slib in $(find %i/lib -name "libtbb_preview.*") ; do
  dlib=$(echo $slib | sed 's|_preview||')
  mv $slib $dlib
done
sed -i -e 's|tbb_preview|tbb|' %{i}/lib/libtbb.so
cmake -DINSTALL_DIR=%{i}/cmake/TBB -DSYSTEM_NAME=Linux -DINC_PATH=%{i}/include -DLIB_PATH=%{i}/lib -P cmake/tbb_config_installer.cmake
