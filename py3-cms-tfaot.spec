### RPM external py3-cms-tfaot 1.0.0
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}

%define github_user riga
%define tag b5b7bb48a1dfe0ddee9277276bbba7f6af826c62
%define branch master
Source: git+https://github.com/%{github_user}/cms-tfaot.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: py3-pip py3-setuptools py3-wheel
Requires: py3-tensorflow py3-cmsml

%prep
%setup -n %{n}-%{realversion}

%build

%install
pip3 install . --prefix=%{i} --no-deps

# copy test models
mkdir -p %{i}/share
cp -r test_models %{i}/share
