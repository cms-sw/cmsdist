### RPM external py3-cms-tfaot 1.0.0
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}

%define github_user riga
%define tag d61fc9898bf315342873812bdd7f7c8cc59ef34f
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
