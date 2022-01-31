### RPM external boost 1.75.0
## INCLUDE compilation_flags
%define tag 3defebd61ecb0970c0046c85384bb34ec9572ac3
%define branch cms/v%realversion
%define github_user cms-externals
Source: git+https://github.com/%github_user/%n.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Patch0: boost-1.75.0-disable-statx
Requires: python3 bz2lib zlib openmpi xz zstd

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
case %cmsos in 
  osx*) TOOLSET=darwin ;;
  *) TOOLSET=gcc ;;
esac

# enable boost::mpi
%if "%{?arch_build_flags:set}" == "set"
echo 'using gcc : : : <cxxflags>"%{arch_build_flags}" ;' > user-config.jam
echo 'using gcc : : : <cflags>"%{arch_build_flags}" ;' >> user-config.jam
%endif

pushd tools/build
  sh bootstrap.sh ${TOOLSET}
  mkdir ./tmp-boost-build
  ./b2 install --prefix=./tmp-boost-build
  export PATH=${PWD}/tmp-boost-build/bin:${PATH}
popd

PYTHONV3=$(echo $PYTHON3_VERSION | cut -f1,2 -d.)

# enable boost::mpi
echo "using mpi ;" >> user-config.jam
echo "using python : ${PYTHONV3} : ${PYTHON3_ROOT}/bin/python3 : ${PYTHON3_ROOT}/include/python${PYTHONV3} : ${PYTHON3_ROOT}/lib ;" >> user-config.jam

b2 -q \
   -d2 \
   %{makeprocesses} \
   --build-dir=build-boost \
   --disable-icu \
   --without-atomic \
   --without-container \
   --without-context \
   --without-coroutine \
   --without-exception \
   --without-graph \
   --without-graph_parallel \
   --without-locale \
   --without-log \
   --without-math \
   --without-random \
   --without-wave \
   --user-config=${PWD}/user-config.jam \
   toolset=${TOOLSET} \
   link=shared \
   threading=multi \
   variant=release \
   python=${PYTHONV3} \
   -sBZIP2_INCLUDE=${BZ2LIB_ROOT}/include \
   -sBZIP2_LIBPATH=${BZ2LIB_ROOT}/lib \
   -sZLIB_INCLUDE=${ZLIB_ROOT}/include \
   -sZLIB_LIBPATH=${ZLIB_ROOT}/lib \
   -sLZMA_INCLUDE=${XZ_ROOT}/include \
   -sLZMA_LIBPATH=${XZ_ROOT}/lib \
   -sZSTD_INCLUDE=${ZSTD_ROOT}/include \
   -sZSTD_LIBPATH=${ZSTD_ROOT}/lib \
   stage

%install
case %{cmsos} in
  osx*) so=dylib ;;
     *) so=so ;;
esac
mkdir -p %{i}/lib %{i}/include
# copy files around in their final location.
# We use tar to reduce the number of processes required
# and because we need to build the build hierarchy for
# the files that we are copying.
pushd stage/lib
  find . -name "*.${so}*" -type f | tar cf - -T - | (cd %{i}/lib; tar xfp -)
popd
find boost -name '*.[hi]*' | tar cf - -T - | ( cd %{i}/include; tar xfp -)

for l in $(find %{i}/lib -name "*.${so}.*")
do
  ln -s $(basename ${l}) $(echo ${l} | sed -e "s|[.]${so}[.].*|.${so}|")
done
