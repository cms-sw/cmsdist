### RPM external simple-proxy-utils 0.1.1
#Source: https://github.com/bbockelm/simple-proxy-utils/archive/master.zip
#Source: https://github.com/vkuznet/simple-proxy-utils/archive/fix-exit-code.zip
Source: https://github.com/bbockelm/simple-proxy-utils/archive/v%realversion.zip
Requires: gcc cmake

# This package relies on the following system packages/RPMs:
# voms-devel, globus-gsi-credential-devel, globus-gsi-cert-utils-devel, globus-common-devel,
# globus-gsi-sysconfig-devel and globus-gsi-callback-devel
Provides: libglobus_common.so.0()(64bit)
Provides: libglobus_common.so.0(GLOBUS_COMMON_14)(64bit)
Provides: libglobus_gsi_callback.so.0()(64bit)
Provides: libglobus_gsi_cert_utils.so.0()(64bit)
Provides: libglobus_gsi_credential.so.1()(64bit)
Provides: libglobus_gsi_sysconfig.so.1()(64bit)
Provides: libvomsapi.so.1()(64bit)

%prep
#%setup -n simple-proxy-utils-master
%setup -n simple-proxy-utils-%realversion

%build
mkdir build
# to avoid incompatibility with system libstdc++ lib
sed -i -e "s,std=c++11,std=c++11 -D_GLIBCXX_USE_CXX11_ABI=0,g" CMakeLists.txt
cd build
cmake ..
make %{makeprocesses}

%install
mkdir %i/lib
cp build/libSimpleProxyUtils.so %i/lib

%define drop_files %i/man
