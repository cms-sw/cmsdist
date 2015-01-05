### RPM lcg roofit 6.02.00
## INITENV +PATH PYTHONPATH %{i}/lib
## INITENV SET ROOTSYS %{i}
%define tag dbb15f91ef4d06cca1a317f421722f1120857b66
%define branch cms/0fa9d45
%define github_user cms-sw
Source: git+https://github.com/%github_user/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isarmv7 %(case %{cmsplatf} in (*armv7*) echo 1 ;; (*) echo 0 ;; esac)

Requires: root

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}

sed -ibak -e 's/\/usr\/local/\/no-no-no\/local/g' \
          -e 's/\/opt\/local/\/no-no-no\/local/g' \
          ./configure

%build
mkdir -p %{i}
export ROOTSYS=%_builddir/root
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)


# Required for generated dictionaries during ROOT6 compile/install
ROOT_INCLUDE_PATH=
for DEP in %requiredtools; do
  ROOT_INCLUDE_PATH=$(eval echo $(printf "\${%%s_ROOT}/include" $(echo $DEP | tr "[a-z]-" "[A-Z]_"))):$ROOT_INCLUDE_PATH
done

export ROOT_INCLUDE_PATH

CONFIG_ARGS="--minimal
             --enable-roofit
             --enable-xml
             --enable-c++11
             --disable-rpath
             --with-cxx=g++
             --with-cc=gcc
             --with-ld=g++
             --with-f77=gfortran
             --with-gcc-toolchain=${GCC_ROOT}"

TARGET_PLATF=

%if %islinux
  TARGET_PLATF=linuxx8664gcc
%endif

%if %isdarwin
  TARGET_PLATF=macosx64
%endif

%if %isarmv7
  TARGET_PLATF=linuxarm
%endif

cat <<\EOF >> MyConfig.mk
CFLAGS+=-D__ROOFIT_NOBANNER
CXXFLAGS+=-D__ROOFIT_NOBANNER
EOF

./configure ${TARGET_PLATF} ${CONFIG_ARGS}

make %{makeprocesses}

%install
mkdir -p %{i}/{lib,bin,include,tutorials}
cp ./lib/{libHistFactory*,libRooFitCore*,libRooFit*,libRooStats*} %{i}/lib
cp ./bin/{prepareHistFactory,hist2workspace} %{i}/bin
rsync -av --exclude='*LinkDef*.h' ./roofit/{roofit,roofitcore,roostats,histfactory}/inc/ %{i}/include/
