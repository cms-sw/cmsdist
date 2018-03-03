### RPM external tbb 2018_U1

%define tag %{realversion}
%define branch tbb_2018
%define github_user 01org
Source: git+https://github.com/%{github_user}/tbb.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

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
