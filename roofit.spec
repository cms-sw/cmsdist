### RPM lcg roofit 5.99.07
## INITENV +PATH PYTHONPATH %{i}/lib
## INITENV SET ROOTSYS %{i}
%define tag 86d37a2c5978890d910c2e902952c5ab749f19e6
%define branch master
Source: git+http://root.cern.ch/git/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isarmv7 %(case %{cmsplatf} in (*armv7*) echo 1 ;; (*) echo 0 ;; esac)

Patch0: root6_patch_v1_for_v5-99-06-380-g509b29c

Requires: root

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}
%patch0 -p0

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
