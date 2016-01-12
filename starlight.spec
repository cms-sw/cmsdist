### RPM external starlight r193
Requires: clhep

%define branch cms/%{realversion}
%define github_user cms-externals
Source0:git+http://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires:	cmake

%define keep_archives true

%prep
%setup -n %{n}/%{realversion}

%build
make %{makeprocess}

%install
make %{make process} install
