### RPM external eigen 3.2.2
## NOCOMPILER
%define tag 17b96fc71403a1be51f15ed0675292b69a6e4d21
%define branch defaultToThreadSafe
%define github_user Dr15Jones
Source: git+https://github.com/%github_user/eigen.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -n %n-%{realversion}

%build
mkdir -p %i/include

%install
cp -r Eigen %i/include

