### RPM external eigen 3.2.2
## NOCOMPILER
%define tag 87b069eefbf748ee3aba16fe5f84b4ccd6227082
%define branch cms/3.2.2
%define github_user cms-externals
Source: git+https://github.com/%github_user/eigen.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -n %n-%{realversion}

%build
mkdir -p %i/include

%install
cp -r Eigen %i/include

