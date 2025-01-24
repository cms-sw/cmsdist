### RPM external gdrcopy 2.4.4
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
Source: https://github.com/NVIDIA/%{n}/archive/v%{realversion}.tar.gz
Requires: cuda

%prep
%setup -n %{n}-%{realversion}

%build
make %{makeprocesses} prefix=%{i} libdir=%{i}/lib64 CUDA=$CUDA_ROOT lib

%install
make %{makeprocesses} prefix=%{i} libdir=%{i}/lib64 CUDA=$CUDA_ROOT lib_install

%post
