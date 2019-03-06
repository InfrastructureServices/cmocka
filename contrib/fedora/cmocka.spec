# would conflict with cmockery2-devel package
%bcond_with     cmockery

Name:           cmocka
Summary:        Unit testing framework for C
Version:        1.1.3
Release:        1%{?dist}
URL:            https://cmocka.org
License:        ASL 2.0

%global major_minor %(echo %{version} | cut -d. -f1-2)
Source0:        https://cmocka.org/files/%{major_minor}/%{name}-%{version}.tar.xz
#
# Git repository: https://git.cryptomilk.org/projects/cmocka.git
BuildRequires:  cmake
BuildRequires:  gcc make
BuildRequires:  doxygen
BuildRequires:  pkgconfig

%description
Cmocka is an elegant unit testing framework for C with support for mock
objects. It only requires the standard C library, works on a range of computing
platforms (including embedded) and with different compilers.

%package devel
Summary:        Lightweight C unit testing framework
Requires:       %{name}%{?_isa} = %{version}-%{release}
Recommends:     cmake
Suggests:       pkgconfig
%if %{with cmockery}
Conflicts:      cmockery2-devel
%endif

%description devel
Cmocka is an elegant unit testing framework for C with support for mock
objects. It only requires the standard C library, works on a range of computing
platforms (including embedded) and with different compilers.

Package provides necessary headers for C unit test development

%package doc
Summary:        Lightweight C unit testing framework
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Cmocka is an elegant unit testing framework for C with support for mock
objects. It only requires the standard C library, works on a range of computing
platforms (including embedded) and with different compilers.

Package provides API documentation and examples

%prep
%autosetup

%build
mkdir build
pushd build
%if %{with cmockery}
%cmake -DWITH_CMOCKERY_SUPPORT=ON ..
%else
%cmake ..
%endif
%make_build
make docs
popd

%install
pushd build
%make_install
popd

%check
ctest -V %{?_smp_mflags}

%ldconfig_scriptlets

%files
%doc README.md INSTALL.md ChangeLog AUTHORS
%license COPYING
%{_libdir}/libcmocka.so.0*

%files devel
%{_includedir}/cmocka*
%if %{with cmockery}
%{_includedir}/cmockery
%endif
%{_libdir}/libcmocka.so
%{_libdir}/pkgconfig/cmocka.pc
%{_libdir}/cmake/cmocka

%files doc
%doc build/doc/html
%doc example/

%changelog
* Wed Mar 06 2019 Petr Menšík <pemensik@redhat.com> - 1.1.3-1
- Initial version

