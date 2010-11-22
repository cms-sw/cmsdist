### RPM external sherpa 1.2.2

#Source: http://cern.ch/service-spi/external/MCGenerators/distribution/sherpa-%{realversion}-src.tgz
Source: http://www.hepforge.org/archive/sherpa/SHERPA-MC-%{realversion}.tar.gz
Patch0: sherpa-1.2.2-add_propagator
Patch1: sherpa-1.2.2-unweighted_events
Requires: hepmc lhapdf

%prep
#%setup -n sherpa/%{realversion}
%setup -q -n SHERPA-MC-%{realversion}
%patch0 -p0
%patch1 -p0
autoreconf -i

# Assumes 32bit for non-amd64, may not be correct for all platforms
case %cmsos in
  slc*_amd64)
   ./configure --prefix=%i --enable-analysis --enable-multithread --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT CXXFLAGS="-O2 -fuse-cxa-atexit"
   ;;
  slc*_ia32)
   ./configure --prefix=%i --enable-analysis --enable-multithread --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT CXXFLAGS="-O2 -fuse-cxa-atexit -m32"
  ;;
  osx10*_ia32)
   ./configure --prefix=%i --enable-analysis --enable-multithread --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT CXXFLAGS="-O2 -fuse-cxa-atexit -m32"
   ;;
  osx10*_amd64)
   ./configure --prefix=%i --enable-analysis --enable-multithread --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT CXXFLAGS="-O2 -fuse-cxa-atexit"
   ;;
  *)
   ./configure --prefix=%i --enable-analysis --enable-multithread --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT CXXFLAGS="-O2 -fuse-cxa-atexit"
esac


%build
# Fix up a configuration mistake coming from a test being confused
# by the "skipping incompatible" linking messages when linking 32bit on 64bit
for file in `find ./ -name Makefile`; do
  perl -p -i -e 's|/usr/lib64/libm.a||' $file
  perl -p -i -e 's|/usr/lib64/libc.a||' $file
done

make %{makeprocesses} 

%install
make install
