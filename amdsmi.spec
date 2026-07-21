## INCLUDE rocm-config
### RPM external amdsmi %{rocm_version_num}
Requires: rocm-core python3 libnl libmnl
%define cmake_args -DBUILD_TESTING=OFF -DCMAKE_SHARED_LINKER_FLAGS="-L$LIBNL_ROOT/lib -L$LIBMNL_ROOT/lib" -DCMAKE_EXE_LINKER_FLAGS="-L$LIBNL_ROOT/lib -L$LIBMNL_ROOT/lib"
## INCLUDE rocm-systems-build
