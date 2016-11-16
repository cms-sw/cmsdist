### RPM external eigen 3.3.0
## NOCOMPILER
%define tag 70dcc5877552891d260d6e212cb81f36553c9514
%define branch cms/3.2.2
%define github_user cms-externals
Source: git+https://github.com/%github_user/eigen.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -n %n-%{realversion}

%build
mkdir -p %i/include

%install
cp -r Eigen %i/include

