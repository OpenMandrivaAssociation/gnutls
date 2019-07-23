%define url_ver %(echo %{version}|cut -d. -f1,2)
%define dirver %(echo %{version}|cut -d. -f1,2,3)
%define _disable_rebuild_configure 1
%define _disable_lto 1

%global optflags %{optflags} -O3 -fuse-ld=bfd
%global ldflags %{ldflags} -fuse-ld=bfd

%define major 30
%define xxmajor 28
%define libname %mklibname %{name} %{major}
%define libnamexx %mklibname %{name}xx %{xxmajor}
%define devname %mklibname %{name} -d

# (tpg) enable PGO build
%bcond_without pgo

Summary:	Library providing a secure layer (SSL)
Name:		gnutls
Version:	3.6.8
Release:	2
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
Url:		http://www.gnutls.org
Source0:	ftp://ftp.gnutls.org/gcrypt/gnutls/v%{url_ver}/%{name}-%{version}.tar.xz
Patch1:		gnutls-3.2.7-rpath.patch
Patch2:		gnutls-3.6.4-clang.patch
# Use only FIPS approved ciphers in the FIPS mode
#Patch7:		gnutls-2.12.21-fips-algorithms.patch
BuildRequires:	bison
BuildRequires:	byacc
BuildRequires:	libunistring-devel
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
#ifnarch %{armx} %{mips} %{riscv}
#BuildRequires:	valgrind
#endif
BuildRequires:	autogen
BuildRequires:	pkgconfig(autoopts)
# (tpg) neeeded for tests
BuildRequires:	iproute2
BuildRequires:	net-tools
BuildRequires:	datefudge
BuildRequires:	gnupg
BuildRequires:	diffutils

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

%prep
%autosetup -n %{name}-%{dirver} -p1

rm -f lib/minitasn1/*.c lib/minitasn1/*.h
rm -f src/libopts/*.c src/libopts/*.h src/libopts/compat/*.c src/libopts/compat/*.h

echo "SYSTEM=NORMAL" >> tests/system.prio

%build
%if %{with pgo}
export LLVM_PROFILE_FILE=%{name}-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)"
CFLAGS="%{optflags} -fprofile-instr-generate" \
CXXFLAGS="%{optflags} -fprofile-instr-generate" \
FFLAGS="$CFLAGS" \
FCFLAGS="$CFLAGS" \
LDFLAGS="%{ldflags} -fprofile-instr-generate" \
%configure \
	--with-included-libtasn1=no \
	--enable-sha1-support \
	--enable-ssl3-support \
	--disable-openssl-compatibility \
	--disable-non-suiteb-curves \
	--disable-rpath \
	--disable-guile \
	--with-default-priority-string="@SYSTEM"

%make_build
make check

unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=%{name}.profile *.profile.d

make clean

CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
LDFLAGS="%{ldflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
%endif
%configure \
	--with-included-libtasn1=no \
	--enable-sha1-support \
	--enable-ssl3-support \
	--disable-openssl-compatibility \
	--disable-non-suiteb-curves \
	--disable-rpath \
	--disable-guile \
	--with-default-priority-string="@SYSTEM"

%make_build LIBS=-ldl

%check
make check V=1

%install
%make_install

%find_lang %{name}

%files
%doc %{_docdir}/%{name}
%{_bindir}/[cgs]*
%{_bindir}/psktool
%{_bindir}/p11tool
%{_bindir}/ocsptool
%{_mandir}/man?/*
%{_infodir}/*

%files locales -f %{name}.lang

%files -n %{libname}
%{_libdir}/libgnutls.so.%{major}*

%files -n %{libnamexx}
%{_libdir}/libgnutlsxx.so.%{xxmajor}*

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gnutls
