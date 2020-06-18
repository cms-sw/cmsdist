### RPM external tbb 2020_U2

%define tag %{realversion}
%define branch tbb_2020
%define github_user oneapi-src
Source: git+https://github.com/%{github_user}/oneTBB.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}

%build

make %{makeprocesses} stdver=c++14

%install
install -d %i/lib
cp -r include %i/include
case %cmsplatf in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac
find build -name "*.$SONAME*" -exec cp {} %i/lib \; 
cmake -DTBB_ROOT=%i -DTBB_OS=Linux -P cmake/tbb_config_generator.cmake 
