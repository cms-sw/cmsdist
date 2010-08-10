### RPM external sherpa 1.2.2
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac 

#Source: http://cern.ch/service-spi/external/MCGenerators/distribution/sherpa-%{realversion}-src.tgz
Source: http://www.hepforge.org/archive/sherpa/SHERPA-MC-%{realversion}.tar.gz

Requires: hepmc lhapdf

%prep
#%setup -n sherpa/%{realversion}
%setup -n SHERPA-MC-%{realversion}

autoreconf -i

# Assumes 32bit for non-amd64, may not be correct for all platforms
case %cmsos in
  slc*_amd64)
   ./configure --prefix=%i --enable-analysis --enable-multithread --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT CXXFLAGS="-O2 -fuse-cxa-atexit"
   ;;
  slc*_ia32)
   ./configure --prefix=%i --enable-analysis --enable-multithread --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT CXXFLAGS="-O2 -fuse-cxa-atexit -m32"
  ;;
  *)
   ./configure --prefix=%i --enable-analysis --enable-multithread --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT CXXFLAGS="-O2 -fuse-cxa-atexit -m32"
esac


%build
case %gccver in
  3.*)
export FC=g77
  ;;
esac

# Fix up a configuration mistake coming from a test being confused
# by the "skipping incompatible" linking messages when linking 32bit on 64bit
for file in `find ./ -name Makefile`; do
  perl -p -i -e 's|/usr/lib64/libm.a||' $file
  perl -p -i -e 's|/usr/lib64/libc.a||' $file
done

make

%install
make install
