### RPM external py3-psutil 5.6.6
## IMPORT build-with-pip3

%define find %i -name '*.egg-info' -delete; \
    find %i -name '.package-checksum' -delete
