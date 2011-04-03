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

# Force architecture based on %%cmsplatf
case %cmsplatf in
  *_amd64_gcc*) ARCH_CMSPLATF="-m64" ;;
  *_ia32_gcc*) ARCH_CMSPLATF="-m32" ;;
esac

./configure --prefix=%i --enable-analysis --enable-multithread \
            --enable-hepmc2=$HEPMC_ROOT --enable-lhapdf=$LHAPDF_ROOT \
            CXXFLAGS="-O2 -fuse-cxa-atexit $ARCH_CMSPLATF"

%build
# Fix up a configuration mistake coming from a test being confused
# by the "skipping incompatible" linking messages when linking 32bit on 64bit
find . -name Makefile -exec perl -p -i -e 's|/usr/lib64/libm.a||g;s|/usr/lib64/libc.a||g;' {} \;

make %{makeprocesses} 

%install
make install
