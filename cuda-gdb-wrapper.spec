### RPM external cuda-gdb-wrapper 1.0

Requires: cuda python

%prep

%build

%install
# add a wrapper for cuda-gdb
mkdir %{i}/bin
cat > %{i}/bin/cuda-gdb << @EOF
#! /bin/bash
export PYTHONHOME=$PYTHON_ROOT
exec $CUDA_ROOT/bin/cuda-gdb.real "\$@"
@EOF
chmod a+x %{i}/bin/cuda-gdb

%post
%{relocateConfig}bin/cuda-gdb
