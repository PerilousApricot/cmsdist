### RPM external bigcouch 0.4.2b

# For what it's worth, I'm completely embarrased by this script
# I'm sure it breaks all kinds of RPM best practices, but this is
# my first RPM script, and it took a lot of work to get here. If someone
# wants to take a stab at cleaning it up, be my guest

Source0: https://github.com/cloudant/bigcouch/archive/bigcouch-%realversion.zip
Source1: bigcouch_cms_auth.erl
Patch0: bigcouch-fix-sconscript
Patch1: bigcouch-add-cmsauth-to-chttpd
# unneeded because the auth is picked up aotomatically
#Patch0: couchdb-cmsauth-Makefile
# Add couch SSL options
## Patch2: couchdb-ssl-client-cert
Patch3: bigcouch-ssl-replication
# add these next two
## Patch4: couchdb-replication-timeout
## Patch5: couchdb-replication-id
# this is already in if you do timeout=unlimited
#Patch4: couchdb-changes-timeout
# need to apply this
## Patch6: couchdb-changes-heartbeat
# this is already included
#Patch6: couchdb-994-db-open-logic-11x
# this neds to be applied
## Patch7: couchdb-changes-retry


# Although there is no technical software dependency,
# couchapp was included because all CMS applications will need it.
Requires: curl spidermonkey openssl icu4c erlang couchapp
BuildRequires: expat gcc zlib

%prep
ls -lah
%setup -n bigcouch-bigcouch-%realversion
%patch0 -p0
%patch3 -p0
ls -lah %{_sourcedir}
cp %{_sourcedir}/bigcouch-add-cmsauth-to-chttpd .
cp %{_sourcedir}/bigcouch_cms_auth.erl .
## cp %{_sourcedir}/132.diff .
#patch -p0 < 132.diff
#cd apps/couch/ ; patch -p0 < %{_sourcedir}/couchdb-ssl-client-cert ; cd -

# patch1 isn't valid till the deps are pulled in
# because it patches chttpd which is a separate repository
# pulled in by rebar (erlang's build system)
#%patch1 -p0
#%patch2 -p0
#%patch3 -p0
#%patch4 -p0
#%patch5 -p0
#%patch6 -p0
#%patch7 -p0
#cp %_sourcedir/couch_cms_auth.erl %_builddir/couchdb/src/couchdb
#perl -p -i -e 's{\s*-L/(opt|usr)/local/lib}{}g; s{-I/(opt|usr)/local/include}{-I/no-no-no/include}g' configure.ac
 
%build
export CURL_ROOT SPIDERMONKEY_ROOT OPENSSL_ROOT ICU4C_ROOT ERLANG_ROOT
wget https://github.com/git/git/archive/v1.8.2-rc3.zip
unzip v1.8.2-rc3
cd git-1.8.2-rc3
mkdir local
make CC=${GCC_ROOT}/bin/cc prefix=`pwd`/local EXPATDIR=${EXPAT_ROOT} OPENSSLDIR=${OPENSSL_ROOT} ZLIBDIR=${ZLIB_ROOT} zlibdir=${ZLIB_ROOT} ZLIB_PATH=${ZLIB_ROOT} CURLDIR=${CURL_ROOT} NO_PERL=1 NO_PYTHON=1 NO_R_TO_GCC_LINKER=1 NEEDS_SSL_WITH_CURL=1 NO_TCLTK=1 %makeprocesses all install
cd ..
mkdir git-wrapper
echo "#!/bin/bash" > git-wrapper/git
GIT_TARGET=`pwd`/git-1.8.2-rc3/local/bin
echo "pwd >> ~/git.log" >> git-wrapper/git
echo "echo args: \$@ >> ~/git.log" >> git-wrapper/git
echo "$GIT_TARGET/git \$@ 2>&1 | tee -a ~/git.log" >> git-wrapper/git
echo "exit 0" >> git-wrapper/git
chmod +x git-wrapper/git
export PATH=`pwd`/git-wrapper:$PATH
which git
echo $PATH
sed -i 's#./rebar#./rebar verbose=1#g' configure
git clone -n https://github.com/cloudant/erlang-oauth.git oauth2
cd oauth2
git checkout -q BigCouch-0.4.0
git describe --always --tags
echo $?
cd ..

cd ..
git init
touch dummy
echo "hi" >> dummy
git add dummy
# bigcouch doesn't seem to want to build from a non-git repository
git commit -m "Dummy"
git tag %realversion
cd -

./configure -p %i
for CONFIG in `find . -name rebar.config`; do
if [[ $CONFIG == './apps/couch/rebar.config' ]]; then
    continue
fi
cat >> $CONFIG <<EOTT

{port_env, [
    {"DRV_CFLAGS", "\$DRV_CFLAGS -I ${ICU4C_ROOT}/include -I ${SPIDERMONKEY_ROOT}/include -I ${CURL_ROOT}/include -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib "},
{"LDFLAGS", " \$LDFLAGS -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib $LDFLAGS"},
{"DRV_LDFLAGS", "\$DRV_LDFLAGS -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib"},

{"DRV_CXXFLAGS", "\$DRV_CXXFLAGS -I ${ICU4C_ROOT}/include -I ${SPIDERMONKEY_ROOT}/include -I ${CURL_ROOT}/include -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib "},
     {"CFLAGS", "\$CFLAGS -I ${ICU4C_ROOT}/include -I ${SPIDERMONKEY_ROOT}/include -I ${CURL_ROOT}/include"}]}.
EOTT

done
export CFLAGS="-I ${ICU4C_ROOT}/include -I ${SPIDERMONKEY_ROOT}/include -I ${CURL_ROOT}/include -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib $CFLAGS"
export LDFLAGS="-L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib $LDFLAGS"
export CXXFLAGS=" -I ${ICU4C_ROOT}/include -I ${SPIDERMONKEY_ROOT}/include -I ${CURL_ROOT}/include -L ${ICU4C_ROOT}/lib -L ${SPIDERMONKEY_ROOT}/lib -L ${CURL_ROOT}/lib $CXXFLAGS"
#--with-js-lib=$SPIDERMONKEY_ROOT/lib --with-js-include=$SPIDERMONKEY_ROOT/include --with-erlang=$ERLANG_ROOT/lib/erlang/usr/include --with-icu4c=$ICU4C_ROOT
which c++
. $GCC_ROOT/etc/profile.d/init.sh
which c++
pwd

sed -i 's#@cat $(appfile) | sed s/%VSN%/`git describe --match 1.*`/ > $(appfile)#@sed -i s/%VSN%/BigCouchTarball/ $(appfile) ; cat $(appfile)#' Makefile
sed -i 's#./rebar#./rebar verbose=1#g' Makefile
sed -i "s#python scons/scons.py#python scons/scons.py spiderLib=${SPIDERMONKEY_ROOT}/lib spiderInclude=${SPIDERMONKEY_ROOT}/include#g" Makefile

echo "STARTING TO MAKE"
echo $PATH
(
cp bigcouch-add-cmsauth-to-chttpd deps/chttpd/src
cp bigcouch_cms_auth.erl deps/chttpd/src/couch_cms_auth.erl
cd deps/chttpd/src
patch -p2 < bigcouch-add-cmsauth-to-chttpd
)

which git
make %makeprocesses
echo "MAKE DONE SON"

%install
if [ ! -e git-1.8.2-rc3 ]; then
    export CURL_ROOT SPIDERMONKEY_ROOT OPENSSL_ROOT ICU4C_ROOT ERLANG_ROOT
    wget https://github.com/git/git/archive/v1.8.2-rc3.zip
    unzip v1.8.2-rc3
    cd git-1.8.2-rc3
    mkdir local
    make CC=${GCC_ROOT}/bin/cc prefix=`pwd`/local EXPATDIR=${EXPAT_ROOT} OPENSSLDIR=${OPENSSL_ROOT} ZLIBDIR=${ZLIB_ROOT} zlibdir=${ZLIB_ROOT} ZLIB_PATH=${ZLIB_ROOT} CURLDIR=${CURL_ROOT} NO_PERL=1 NO_PYTHON=1 NO_R_TO_GCC_LINKER=1 NEEDS_SSL_WITH_CURL=1 NO_TCLTK=1 %makeprocesses all install
    cd ..
    mkdir git-wrapper
    echo "#!/bin/bash" > git-wrapper/git
    GIT_TARGET=`pwd`/git-1.8.2-rc3/local/bin
    echo "pwd >> ~/git.log" >> git-wrapper/git
    echo "echo args: \$@ >> ~/git.log" >> git-wrapper/git
    echo "$GIT_TARGET/git \$@ 2>&1 | tee -a ~/git.log" >> git-wrapper/git
    echo "exit 0" >> git-wrapper/git
    chmod +x git-wrapper/git
fi
export PATH=`pwd`/git-wrapper:$PATH
which git

make %makeprocesses install
%define drop_files %i/{man,share/doc}

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
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

%post
 
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
%{relocateConfig}etc/profile.d/init.*sh
%{relocateConfig}etc/default.ini
#%{relocateConfig}lib/couch/ebin/couch.app
#%{relocateConfig}bin/bigcouch
#%{relocateConfig}bin/couchjs
#%{relocateConfig}releases/*/*
