### RPM external xz-bootstrap 5.0.3__5.1.2alpha
%define generic_version 5.0.3
%define fcarm_version 5.1.2alpha
Source0: http://tukaani.org/xz/xz-%{generic_version}.tar.gz
Source1: http://tukaani.org/xz/xz-%{fcarm_version}.tar.gz

%define isfcarm %(case %{cmsplatf} in (fc*_arm*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%if %isfcarm
%setup -b 1 -n xz-%{fcarm_version}
%else
%setup -b 0 -n xz-%{generic_version}
%endif

%build
./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
