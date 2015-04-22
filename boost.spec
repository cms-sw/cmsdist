### RPM external boost 1.57.0

%define tag 040a06a
%define branch cms/v%realversion
%define github_user cms-externals
Source: git+https://github.com/%github_user/%n.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++11 -O2
%endif

Requires: python bz2lib zlib

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

b2 -q \
   -d2 \
   %{makeprocesses} \
   --build-dir=build-boost \
   --disable-icu \
   --without-atomic \
   --without-chrono \
   --without-container \
   --without-context \
   --without-coroutine \
   --without-exception \
   --without-graph \
   --without-graph_parallel \
   --without-locale \
   --without-log \
   --without-math \
   --without-mpi \
   --without-random \
   --without-wave \
   toolset=${TOOLSET} \
   link=shared \
   threading=multi \
   variant=release \
   cxxflags="%{cms_cxxflags}" \
   -sBZIP2_INCLUDE=${BZ2LIB_ROOT}/include \
   -sBZIP2_LIBPATH=${BZ2LIB_ROOT}/lib \
   -sZLIB_INCLUDE=${ZLIB_ROOT}/include \
   -sZLIB_LIBPATH=${ZLIB_ROOT}/lib \
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

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %{i}/etc/profile.d
: > %{i}/etc/profile.d/dependencies-setup.sh
: > %{i}/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
