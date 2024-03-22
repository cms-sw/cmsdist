### RPM external py3-cms-tfaot 1.0.0
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}

%define github_user riga
%define tag a2bbd06cbed0efa1fa191cc2f50a6b03067e59d2
%define branch master
Source: git+https://github.com/%{github_user}/cms-tfaot.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: py3-pip py3-setuptools py3-wheel
Requires: py3-cmsml py3-tensorflow

%prep
%setup -n %{n}-%{realversion}

%build

%install
pip3 install . --prefix=%{i} --no-deps

# copy test models
mkdir -p %{i}/share
cp -r test_models %{i}/share
