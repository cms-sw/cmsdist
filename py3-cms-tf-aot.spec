### RPM external py3-cms-tf-aot 0.1.0
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}

%define github_user riga
%define tag ac5e4ed8507ad63be5814247ef32cb9d0ecc21ff
%define branch dev
Source: git+https://github.com/%{github_user}/cms-tf-aot.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: py3-pip py3-setuptools py3-wheel
Requires: py3-tensorflow py3-cmsml

%prep
%setup -n %{n}-%{realversion}

%build

%install
pip3 install . --prefix=%{i} --no-deps
