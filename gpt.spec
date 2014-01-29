### RPM external gpt 3.2
## INITENV SET GPT_LOCATION %i
Source: ftp://ftp.ncsa.uiuc.edu/aces/gpt/releases/gpt-3.2/%n-%v-src.tar.gz
%build
export GPT_LOCATION=%i
./build_gpt
%install
perl -p -i -e "s|^#!.*perl|#!/usr/bin/env perl|" $(find %i/sbin) 
