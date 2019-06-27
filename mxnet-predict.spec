### RPM external mxnet-predict 1.2.1
%define tag 97171b96b2b7efc78eccfbe0a0c2561a377ce153
%define branch 1.2.1.mod3
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/incubator-mxnet.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

Requires: OpenBLAS

%prep
%setup -q -n %{n}-%{realversion}

%build
make %{makeprocesses} USE_OPENCV=0 USE_OPENMP=0 USE_BLAS=openblas USE_CPP_PACKAGE=1 USE_F16C=0 \
    ADD_LDFLAGS="-L$OPENBLAS_ROOT/lib" \
    ADD_CFLAGS="-I$OPENBLAS_ROOT/include -DDISABLE_OPENMP=1 -DMSHADOW_RABIT_PS=0 -DMSHADOW_DIST_PS=0 -DMXNET_PREDICT_ONLY=1 -DMXNET_THREAD_LOCAL_ENGINE=1"

%install
mkdir -p %{i}/{lib,include}
mv lib/libmxnet.so                  %{i}/lib/libmxnetpredict.so
mv include/*                        %{i}/include
mv 3rdparty/dmlc-core/include/*     %{i}/include
mv 3rdparty/tvm/nnvm/include/*      %{i}/include
mv cpp-package/include/*            %{i}/include


# bla bla
