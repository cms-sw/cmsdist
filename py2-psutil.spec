### RPM external py2-psutil 5.0.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

%define git_repo giampaolo
%define git_branch master
%define git_commit release-5.0.0
Source: git://github.com/%{git_repo}/psutil.git?obj=%{git_branch}/%{git_commit}&export=%{n}-%{git_commit}&output=/%{n}-%{git_commit}.tar.gz

Requires: python
BuildRequires: py2-setuptools

%prep
%setup -n %{n}-%{git_commit}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%{i}
find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -type d -print0 | xargs -0 rm -rf
