### RPM external condor 8.0.4
## INITENV +PATH LD_LIBRARY_PATH %i/lib
## INITENV +PATH LD_LIBRARY_PATH %i/lib/condor
## INITENV +PATH PYTHONPATH %i/lib/python

%define _default_patch_fuzz 2
%define condortag V8_0_3

%global __requires_exclude libkeyutils\\.so.*|libsasl2\\.so.*|libselinux\\.so.*

Source: git://github.com/htcondor/htcondor.git?obj=master/%{condortag}&export=condor-%{realversion}&output=/condor-%{realversion}.tar.gz
Patch0: cms-htcondor-build

Requires: openssl zlib
Requires: cmake gcc
Requires: python
Requires: libtool
Requires: p5-archive-tar
Requires: expat

%prep 
%setup -n %n-%{realversion}
%patch0 -p1
sed -i "s,P5_ARCHIVE_TAR_ROOT,$P5_ARCHIVE_TAR_ROOT," externals/bundles/globus/5.2.1/CMakeLists.txt
sed -i "s,P5_IO_ZLIB_ROOT,$P5_IO_ZLIB_ROOT," externals/bundles/globus/5.2.1/CMakeLists.txt
sed -i "s,P5_PACKAGE_CONSTANTS_ROOT,$P5_PACKAGE_CONSTANTS_ROOT," externals/bundles/globus/5.2.1/CMakeLists.txt
sed -i "s,ENVLD_LIBRARY_PATH,$LD_LIBRARY_PATH," externals/bundles/globus/5.2.1/CMakeLists.txt
sed -i "s,LIBTOOL_ROOT,$LIBTOOL_ROOT,g" externals/bundles/globus/5.2.1/CMakeLists.txt
sed -i "s,OPENSSL_ROOT,$OPENSSL_ROOT,g" externals/bundles/globus/5.2.1/CMakeLists.txt
sed -i "s,EXPAT_ROOT,$EXPAT_ROOT,g" externals/bundles/voms/2.0.6/CMakeLists.txt

%build
mkdir -p cmake_build
cd cmake_build

# Fix perl libraries for globus which doesn't search PERL%LIB
mkdir -p build/bld_external/globus-5.2.1-p1/install/lib/perl
ln -sf $P5_ARCHIVE_TAR_ROOT/lib/perl5/Archive build/bld_external/globus-5.2.1-p1/install/lib/perl
ln -sf $P5_IO_ZLIB_ROOT/lib/perl5/IO build/bld_external/globus-5.2.1-p1/install/lib/perl
ln -sf $P5_PACKAGE_CONSTANTS_ROOT/lib/perl5/Package build/bld_external/globus-5.2.1-p1/install/lib/perl

CMAKE_LIBRARY_PATH=${OPENSSL_ROOT}/lib:${LIBTOOL_ROOT}/lib \
cmake ../ \
  -DCMAKE_INSTALL_PREFIX=%i \
  -DUW_BUILD:BOOL=ON \
  -DWITH_GLOBUS:BOOL=ON \
  -DWITH_CREAM:BOOL=OFF \
  -DWITH_PYTHON_BINDINGS:BOOL=ON \
  -DWITH_VOMS:BOOL=OFF \
  -DHAVE_SSH_TO_JOB:BOOL=OFF \
  -DWITH_COREDUMPER:BOOL=OFF \
  -DWITH_DRMAA:BOOL=OFF \
  -DWITH_GSOAP:BOOL=OFF \
  -DWITH_BLAHP:BOOL=OFF \
  -DWITH_KRB5:BOOL=OFF \
  -DWITH_OPENSSL:BOOL=ON \
  -DWITH_LIBCGROUP:BOOL=OFF \
  -DWITH_LIBVIRT:BOOL=OFF \
  -DLDAP_FOUND_SEARCH_lber:PATH=LDAP_FOUND_SEARCH_lber-NOTFOUND \
  -DLDAP_FOUND_SEARCH_ldap:PATH=LDAP_FOUND_SEARCH_ldap-NOTFOUND \
  -DWITH_UNICOREGAHP:BOOL=OFF \
  -DWITH_LIBDELTACLOUD:BOOL=OFF \
  -DPYTHON_EXECUTABLE:FILEPATH=${PYTHON_ROOT}/bin/python2.6 \
  -DPYTHON_INCLUDE_DIR:PATH=${PYTHON_ROOT}/include/python2.6 \
  -DPYTHON_LIBRARY:FILEPATH=${PYTHON_ROOT}/lib/libpython2.6.so \
  -DEXPAT_FOUND_SEARCH_expat:FILEPATH=${EXPAT_ROOT}/lib/libexpat.so \
  -DCLIPPED:BOOL=ON

# Use makeprocess macro, it uses compiling_processes defined by
# build configuration file or build argument
make %makeprocesses VERBOSE=1 externals
make %makeprocesses VERBOSE=1

%install
cd cmake_build
make install
cd ..

rm -rf %i/etc %i/examples %i/include
rm -rf %i/sbin
rm -rf %i/libexec
rm -rf %i/src %i/bosco* %i/condor*
rm -rf %i/lib/condor/{libcom*,libcrypto*,libexpat*,libk*,libl*,libp*,libssl*,libgssapi_krb5*}

# make dummy condor_config
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done
echo "# Dummy condor_config for CMS installs" > %i/etc/condor_config_blank
cat << 'EOF' >> %i/etc/profile.d/dependencies-setup.sh
if [[ ! -f $CONDOR_CONFIG && ! -f /etc/condor/condor_config && ! -f $HOME/condor/condor_config ]]; then
    export CONDOR_CONFIG=%i/etc/condor_config_blank
fi
EOF

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

