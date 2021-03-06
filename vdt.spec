### RPM cms vdt v0.3.2

Source: svn://svnweb.cern.ch/guest/%{n}/tags/%{realversion}?scheme=http&strategy=export&module=%{n}&output=/%{n}-%{realversion}.tar.gz

BuildRequires: cmake

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%define keep_archives true

%prep
%setup -q -n %{n}

%build
%ifarch i386 i486 i585 i686 x86_64
cmake . \
  -DCMAKE_CXX_COMPILER="%{cms_cxx}" \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DPRELOAD:BOOL=ON \
  -DSSE:BOOL=ON 
%endif

%ifarch %{arm}
cmake . \
  -DCMAKE_CXX_COMPILER="%{cms_cxx}" \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DPRELOAD:BOOL=ON \
  -DSSE:BOOL=OFF
%endif

make %{makeprocesses} VERBOSE=1

%install
make install
