%define url_ver %(echo %{version}|cut -d. -f1,2)
%define dirver %(echo %{version}|cut -d. -f1,2,3)
%define _disable_rebuild_configure 1
%global optflags %{optflags} -O3

%define major 30
%define xxmajor 28
%define libname %mklibname %{name} %{major}
%define libnamexx %mklibname %{name}xx %{xxmajor}
%define devname %mklibname %{name} -d

Summary:	Library providing a secure layer (SSL)
Name:		gnutls
Version:	3.6.5
Release:	3
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
%ifnarch %{arm} %{mips} aarch64
BuildRequires:	valgrind
%endif
BuildRequires:	autogen
BuildRequires:	pkgconfig(autoopts)

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
%configure \
	--with-included-libtasn1=no \
	--enable-sha1-support \
	--enable-ssl3-support \
	--disable-openssl-compatibility \
%ifnarch %{arm} %{mips} aarch64
	--enable-valgrind-tests \
%endif
	--disable-non-suiteb-curves \
	--disable-rpath \
	--disable-guile \
	--with-default-priority-string="@SYSTEM"

%make_build

%check
#make check

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
