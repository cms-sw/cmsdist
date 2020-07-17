### RPM external boost 1.72.0

%define tag aa7b52bed9af4b0b1de19cde86f63466a1c33452
%define branch cms/v%realversion.modules
%define github_user cms-externals
Source: git+https://github.com/%github_user/%n.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: python bz2lib zlib openmpi xz zstd

%prep
%setup -n %{n}-%{realversion}

%build
case %cmsos in 
  osx*) TOOLSET=darwin ;;
  *) TOOLSET=gcc ;;
esac

pushd tools/build
  sh bootstrap.sh ${TOOLSET}
  mkdir ./tmp-boost-build
  ./b2 install --prefix=./tmp-boost-build
  export PATH=${PWD}/tmp-boost-build/bin:${PATH}
popd

# enable boost::mpi
echo "using mpi ;" > user-config.jam

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
