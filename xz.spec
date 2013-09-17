### RPM external xz 5.0.3__5.1.2alpha
%define generic_version 5.0.3
%define fc18arm_version 5.1.2alpha
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source0: http://tukaani.org/%{n}/%{n}-%{generic_version}.tar.gz
Source1: http://tukaani.org/%{n}/%{n}-%{fc18arm_version}.tar.gz

%define isfc18arm %(case %{cmsplatf} in (fc18_arm*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%if %isfc18arm
%setup -b 1 -n %{n}-%{fc18arm_version}
%else
%setup -b 0 -n %{n}-%{generic_version}
%endif

%build
case %{cmsplatf} in
   *_mic_* )
    CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ./configure CFLAGS='-fPIC -Ofast' --prefix=%i --disable-static --host=x86_64-k1om-linux
     ;;
   * )
     ./configure CFLAGS='-fPIC -Ofast' --prefix=%i --disable-static
     ;;
esac
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
