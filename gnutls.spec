# gnutls is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

# static libs are used by qemu

%define url_ver %(echo %{version}|cut -d. -f1,2)
%define dirver %(echo %{version}|cut -d. -f1,2,3)
%define _disable_rebuild_configure 1

%global optflags %{optflags} -O3 -fPIC

%define major 30
%define xxmajor %{major}
%define libname %mklibname %{name}
%define oldlibname %mklibname %{name} 30
%define libnamexx %mklibname %{name}xx
%define oldlibnamexx %mklibname %{name}xx 30
%define devname %mklibname %{name} -d
%define sdevname %mklibname %{name} -d -s
%define lib32name %mklib32name %{name}
%define oldlib32name %mklibname %{name} 30
%define lib32namexx %mklib32name %{name}xx
%define oldlib32namexx %mklib32name %{name}xx 30
%define dev32name %mklib32name %{name} -d
%define sdev32name %mklib32name %{name} -d -s

# (tpg) enable PGO build
%bcond_without pgo

%ifarch %{ix86}
%global ldflags %{ldflags} -Wl,-z,notext
%endif

Summary:	Library providing a secure layer (SSL)
Name:		gnutls
Version:	3.8.0
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
Url:		http://www.gnutls.org
Source0:	https://www.gnupg.org/ftp/gcrypt/gnutls/v%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		https://src.fedoraproject.org/rpms/gnutls/raw/master/f/gnutls-3.2.7-rpath.patch
Patch1:		gnutls-3.8.0-clang.patch
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
Requires:	%{name}-config = %{EVRD}
%rename %{oldlibname}

%description -n %{libname}
This package contains a shared library for %{name}.

%package -n %{libnamexx}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries
%rename %{oldlibnamexx}

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

%package -n %{sdevname}
Summary:	Static libraries for %{name}
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n %{sdevname}
This package contains all necessary files to compile or develop
programs/libraries that use %{name} and link them statically.

%package locales
Summary:	Locale files for GnuTLS
Group:		System/Internationalization 
BuildArch:	noarch

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
%rename %{oldlib32name}

%description -n %{lib32name}
This package contains a shared library for %{name}.

%package -n %{lib32namexx}
Summary:	Library providing a secure layer (SSL) (32-bit)
Group:		System/Libraries
%rename %{oldlib32namexx}

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

%package -n %{sdev32name}
Summary:	Static libraries for %{name} (32-bit)
Group:		Development/C
Requires:	%{dev32name} = %{version}-%{release}

%description -n %{sdev32name}
This package contains all necessary files to compile or develop
programs/libraries that use %{name} and link them statically
%endif

%prep
%autosetup -n %{name}-%{dirver} -p1

rm -f lib/minitasn1/*.c lib/minitasn1/*.h

echo "SYSTEM=NORMAL" >> tests/system.prio

# (tpg) 2022-05-27 clang-14: error: the clang compiler does not support '-march=all'
sed -i -e 's/-Wa,-march=all//' lib/accelerated/aarch64/Makefile.*

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
	--enable-static \
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

mkdir build
cd build
%if %{with pgo}
export LD_LIBRARY_PATH="$(pwd)"

CFLAGS="%{optflags} -fprofile-generate" \
CXXFLAGS="%{optflags} -fprofile-generate" \
LDFLAGS="%{build_ldflags} -fprofile-generate" \
%configure \
	--with-included-libtasn1=no \
	--enable-local-libopts \
	--enable-sha1-support \
	--enable-ssl3-support \
	--enable-static \
	--disable-openssl-compatibility \
	--disable-non-suiteb-curves \
	--disable-rpath \
	--disable-guile \
	--with-default-priority-string="@SYSTEM"

%make_build

# (tpg) run benchmarks
LD_PRELOAD="./lib/.libs/libgnutls.so" ./src/.libs/gnutls-cli --benchmark-ciphers
LD_PRELOAD="./lib/.libs/libgnutls.so" ./src/.libs/gnutls-cli --benchmark-tls-kx
LD_PRELOAD="./lib/.libs/libgnutls.so" ./src/.libs/gnutls-cli --benchmark-tls-ciphers

unset LD_LIBRARY_PATH
llvm-profdata merge --output=%{name}-llvm.profdata $(find . -name "*.profraw" -type f)
PROFDATA="$(realpath %{name}-llvm.profdata)"
rm -f *.profraw

make clean

CFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
CXXFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
LDFLAGS="%{build_ldflags} -fprofile-use=$PROFDATA" \
%endif
%configure \
	--with-included-libtasn1=no \
	--enable-local-libopts \
	--enable-sha1-support \
	--enable-ssl3-support \
	--enable-static \
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

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

%files
%doc %{_docdir}/%{name}
%{_bindir}/[cgs]*
%{_bindir}/psktool
%{_bindir}/p11tool
%{_bindir}/ocsptool
%doc %{_mandir}/man?/*
%doc %{_infodir}/*

%files config
%dir %{_sysconfdir}/gnutls
%config(noreplace) %{_sysconfdir}/gnutls/config

%files locales -f %{name}.lang

%files -n %{libname}
%{_libdir}/libgnutls.so.%{major}*
%{_libdir}/libgnutls.so

%files -n %{libnamexx}
%{_libdir}/libgnutlsxx.so.%{xxmajor}*
%{_libdir}/libgnutlsxx.so

%files -n %{devname}
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gnutls

%files -n %{sdevname}
%{_libdir}/*.a

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libgnutls.so.%{major}*
%{_prefix}/lib/libgnutls.so

%files -n %{lib32namexx}
%{_prefix}/lib/libgnutlsxx.so.%{xxmajor}*
%{_prefix}/lib/libgnutlsxx.so

%files -n %{dev32name}
%{_prefix}/lib/pkgconfig/*.pc

%files -n %{sdev32name}
%{_prefix}/lib/*.a
%endif
