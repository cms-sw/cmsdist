### RPM external naturalearthdata 20120502
## NOCOMPILER

%define site www.naturalearthdata.com
Source0: http://%site/http//%site/download/110m/cultural/110m-cultural.zip
Source1: http://%site/http//%site/download/110m/physical/110m-physical.zip
Source2: http://%site/http//%site/download/50m/cultural/50m-cultural.zip
Source3: http://%site/http//%site/download/50m/physical/50m-physical.zip
#Source4: http://%site/http//%site/download/10m/cultural/10m-cultural.zip
#Source5: http://%site/http//%site/download/10m/physical/10m-physical.zip

%prep
%setup    -T -b 0 -n 110m_cultural
%setup -D -T -b 1 -n 110m_physical
%setup -D -T -b 2 -n 50m_cultural
%setup -D -T -b 3 -n 50m_physical
#%setup -D -T -b 4 -n 10m_cultural
#%setup -D -T -b 5 -n 10m_physical

%build

%install
cd ..
mkdir -p %i/data
#cp -rp {10,50,110}m_{cultural,physical} %i/data
cp -rp {50,110}m_{cultural,physical} %i/data
find %i/data -type f -exec chmod 644 {} \;
