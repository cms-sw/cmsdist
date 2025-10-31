%define git_remote https://github.com/alpaka-group/alpaka
%define git_branch develop
%define git_commit %(git ls-remote %{git_remote}.git refs/heads/%{git_branch} | cut -c-40)
%define git_short  %(echo %{git_commit} | cut -c-11)
### RPM external alpaka %{git_branch}-%{git_short}
## NOCOMPILER

Source: %{git_remote}/archive/%{git_commit}.tar.gz

%prep
%setup -n %{n}-%{git_commit}

%build

%install
cp -ar include %{i}/include

%post
