### RPM external gdrcopy 2.1
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
Source: https://github.com/NVIDIA/%{n}/archive/v%{realversion}.tar.gz
Requires: cuda

%prep
%setup -n %{n}-%{realversion}

%build
make %{makeprocesses} PREFIX=%{i} CUDA=$CUDA_ROOT lib

%install
make %{makeprocesses} PREFIX=%{i} CUDA=$CUDA_ROOT lib_install

%post
