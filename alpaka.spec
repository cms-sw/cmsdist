### RPM external alpaka develop-20230209
## NOCOMPILER

%define git_commit d1855b1b0d0a2877b06147eacf0ddda56e40d661

Source: https://github.com/cms-patatrack/%{n}/archive/%{git_commit}.tar.gz
Requires: boost

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
