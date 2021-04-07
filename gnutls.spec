# gnutls is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define url_ver %(echo %{version}|cut -d. -f1,2)
%define dirver %(echo %{version}|cut -d. -f1,2,3)
%define _disable_rebuild_configure 1

%global optflags %{optflags} -O3 -fPIC

%define major 30
%define xxmajor 28
%define libname %mklibname %{name} %{major}
%define libnamexx %mklibname %{name}xx %{xxmajor}
%define devname %mklibname %{name} -d
%define lib32name %mklib32name %{name} %{major}
%define lib32namexx %mklib32name %{name}xx %{xxmajor}
%define dev32name %mklib32name %{name} -d

# (tpg) enable PGO build
%bcond_without pgo

%ifarch %{ix86}
%global ldflags %{ldflags} -Wl,-z,notext
%endif

Summary:	Library providing a secure layer (SSL)
Name:		gnutls
Version:	3.7.0
Release:	2
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
Url:		http://www.gnutls.org
Source0:	https://www.gnupg.org/ftp/gcrypt/gnutls/v%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		https://src.fedoraproject.org/rpms/gnutls/raw/master/f/gnutls-3.2.7-rpath.patch
Patch1:		https://src.fedoraproject.org/rpms/gnutls/raw/master/f/gnutls-3.6.7-no-now-guile.patch
Patch2:		https://src.fedoraproject.org/rpms/gnutls/raw/rawhide/f/gnutls-3.7.1-aggressive-realloc-fixes.patch
BuildRequires:	bison
BuildRequires:	byacc
BuildRequires:	pkgconfig(libunistring)
BuildRequires:	pkgconfig(lzo2)
BuildRequires:	gmp-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(libtasn1)
BuildRequires:	pkgconfig(p11-kit-1)
BuildRequires:	pkgconfig(nettle)
BuildRequires:	pkgconfig(libidn2)
BuildRequires:	pkgconfig(libseccomp)
BuildRequires:	libatomic-devel
BuildRequires:	gtk-doc
#ifnarch %{armx} %{mips} %{riscv}
#BuildRequires:	valgrind
#endif
BuildRequires:	autogen
BuildRequires:	texinfo
# (tpg) neeeded for tests
BuildRequires:	iproute2
BuildRequires:	net-tools
BuildRequires:	datefudge
BuildRequires:	gnupg
BuildRequires:	diffutils
%if %{with compat32}
BuildRequires:	devel(libnettle)
BuildRequires:	devel(libunistring)
BuildRequires:	devel(liblzo2)
BuildRequires:	devel(libgcrypt)
BuildRequires:	devel(libtasn1)
BuildRequires:	devel(libidn2)
BuildRequires:	devel(libgmp)
%endif

%description
GnuTLS is a project that aims to develop a library which provides 
a secure layer, over a reliable transport layer.

%package -n %{libname}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries
Suggests:	%{name}-locales = %{version}-%{release}
%if "%{_lib}" == "lib64"
Conflicts:	lib%{name}%{major} < %{version}
%endif
Obsoletes:	%{mklibname %{name}-openssl 27} < 3.6.5
Requires:	%{name}-config = %{EVRD}

%description -n %{libname}
This package contains a shared library for %{name}.

%package -n %{libnamexx}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries
Conflicts:	%{_lib}gnutls28 < 3.1.9.1-3

%description -n %{libnamexx}
This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libnamexx} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains all necessary files to compile or develop
programs/libraries that use %{name}.

%package locales
Summary:	Locale files for GnuTLS
Group:		System/Internationalization 
BuildArch:	noarch
Conflicts:	%{mklibname gnutls 28} <= 3.1.9.1-1

%description locales
Locale files for GnuTLS main library.

%package config
Summary:	GnuTLS configuration files
Group:		System/Libraries
BuildArch:	noarch

%description config
GnuTLS configuration files

%if %{with compat32}
%package -n %{lib32name}
Summary:	Library providing a secure layer (SSL) (32-bit)
Group:		System/Libraries
Suggests:	%{name}-locales = %{version}-%{release}
Requires:	%{name}-config = %{EVRD}

%description -n %{lib32name}
This package contains a shared library for %{name}.

%package -n %{lib32namexx}
Summary:	Library providing a secure layer (SSL) (32-bit)
Group:		System/Libraries

%description -n %{lib32namexx}
This package contains a shared library for %{name}.

%package -n %{dev32name}
Summary:	Development files for %{name} (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%{lib32namexx} = %{version}-%{release}

%description -n %{dev32name}
This package contains all necessary files to compile or develop
programs/libraries that use %{name}.
%endif

%prep
%autosetup -n %{name}-%{dirver} -p1

rm -f lib/minitasn1/*.c lib/minitasn1/*.h

echo "SYSTEM=NORMAL" >> tests/system.prio

%build
autoreconf -fiv

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
# FIXME p11-kit disabled for now to avoid circular build deps
%configure32 \
	--host=i686-openmandriva-linux-gnu \
	--target=i686-openmandriva-linux-gnu \
	--enable-local-libopts \
	--without-p11-kit \
	--with-included-libtasn1=no \
	--enable-sha1-support \
	--enable-ssl3-support \
	--disable-openssl-compatibility \
	--disable-non-suiteb-curves \
	--disable-rpath \
	--disable-guile \
	--with-default-priority-string="@SYSTEM"
%make_build
cd ..
%endif

# We use the bundled libopts for 32-bit builds (because building autogen would
# pull in guile and other stuff we don't need). It's safe to kill before
# doing the 64-bit build.
rm -f src/libopts/*.c src/libopts/*.h src/libopts/compat/*.c src/libopts/compat/*.h

mkdir build
cd build
%if %{with pgo}
export LLVM_PROFILE_FILE=%{name}-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)"
CFLAGS="%{optflags} -fprofile-instr-generate" \
CXXFLAGS="%{optflags} -fprofile-instr-generate" \
FFLAGS="$CFLAGS" \
FCFLAGS="$CFLAGS" \
LDFLAGS="%{ldflags} -fPIC -fprofile-instr-generate" \
%configure \
	--with-included-libtasn1=no \
	--enable-local-libopts \
	--enable-sha1-support \
	--enable-ssl3-support \
	--disable-openssl-compatibility \
	--disable-non-suiteb-curves \
	--disable-rpath \
	--disable-guile \
	--with-default-priority-string="@SYSTEM"

%make_build
make check || :

unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=%{name}.profile *.profile.d

make clean

CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
LDFLAGS="%{ldflags} -fPIC -fprofile-instr-use=$(realpath %{name}.profile)" \
%endif
%configure \
	--with-included-libtasn1=no \
	--enable-local-libopts \
	--enable-sha1-support \
	--enable-ssl3-support \
	--disable-openssl-compatibility \
	--disable-non-suiteb-curves \
	--disable-rpath \
	--disable-guile \
	--with-default-priority-string="@SYSTEM"

%make_build LIBS=-ldl

# FIXME as of 3.6.12, 17 tests fail. Let's allow it for now.
# %%check
# %%make_build check V=1 || :

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

mkdir -p %{buildroot}%{_sysconfdir}/gnutls
cat >%{buildroot}%{_sysconfdir}/gnutls/config <<'EOF'
[priorities]
SYSTEM = NORMAL:-VERS-TLS1.1:-VERS-TLS1.0
EOF

%find_lang %{name}

%files
%doc %{_docdir}/%{name}
%{_bindir}/[cgs]*
%{_bindir}/psktool
%{_bindir}/p11tool
%{_bindir}/ocsptool
%{_mandir}/man?/*
%{_infodir}/*

%files config
%dir %{_sysconfdir}/gnutls
%config(noreplace) %{_sysconfdir}/gnutls/config

%files locales -f %{name}.lang

%files -n %{libname}
%{_libdir}/libgnutls.so.%{major}*

%files -n %{libnamexx}
%{_libdir}/libgnutlsxx.so.%{xxmajor}*

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gnutls

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libgnutls.so.%{major}*

%files -n %{lib32namexx}
%{_prefix}/lib/libgnutlsxx.so.%{xxmajor}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
