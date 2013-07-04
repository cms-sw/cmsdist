### RPM external xz 5.0.3__5.1.2alpha
%define generic_version 5.0.3
%define fc18arm_version 5.1.2alpha
Source0: http://tukaani.org/%{n}/%{n}-%{generic_version}.tar.xz
Source1: http://tukaani.org/%{n}/%{n}-%{fc18arm_version}.tar.xz

%define isfc18arm %(case %{cmsplatf} in (fc18_arm*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%if %isfc18arm
%setup -b 1 -n %{n}-%{fc18arm_version}
%else
%setup -b 0 -n %{n}-%{generic_version}
%endif

%build
./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
