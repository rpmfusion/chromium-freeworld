#Global Libraries
#Do not turn it on in Fedora copr!
%global freeworld 1
%global menu_name Chromium (Freeworld)
%global xdg_subdir chromium
%ifarch aarch64
%global _smp_build_ncpus 6
%endif
#This can be any folder on out
%global target out/Release
### Google API keys (see http://www.chromium.org/developers/how-tos/api-keys)
### Note: These are for Fedora use ONLY.
### For your own distribution, please get your own set of keys.
### http://lists.debian.org/debian-legal/2013/11/msg00006.html
%global api_key AIzaSyDUIXvzVrt5OkVsgXhQ6NFfvWlA44by-aw
###############################Exclude Private chromium libs###########################
%global __requires_exclude %{chromiumdir}/.*\\.so
%global __provides_exclude_from %{chromiumdir}/.*\\.so
#######################################CONFIGS###########################################
# System libraries to use.
%global system_ffmpeg 1
%global system_freetype 0
%if 0%{?fedora} >= 36
%global system_harfbuzz 1
%else
%global system_harfbuzz 0
%endif
%global system_libicu 0
%global system_libvpx 0
%global system_libxml2 1
%global system_minizip 1
%global system_re2 1
##############################Package Definitions######################################
Name:           chromium-freeworld
Version:        94.0.4606.61
Release:        1%{?dist}
Summary:        Chromium built with all freeworld codecs and VA-API support
License:        BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:            https://www.chromium.org/Home

%if %{freeworld}
Source0:        https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%else
# Unfortunately, Fedora & Copr forbids uploading sources with patent-encumbered
# ffmpeg code even if they are never compiled and linked to target binaries,
# so we must repackage upstream tarballs to satisfy this requirement. However,
# we cannot simply delete all code of ffmpeg because this will disable support
# for some commonly-used free codecs such as Ogg Theora. Instead, helper
# scripts included in official Fedora packages are copied, modified, and used
# to automate the repackaging work.
# Get those helper scripts from https://src.fedoraproject.org/rpms/chromium
# If you don't use Fedora services, Just set the value of freeworld in this spec file
# to 1 to use the upstreanm packaged source.
# The repackaged source tarball used here is produced by:
# ./chromium-latest.py --stable --ffmpegclean --ffmpegarm --deleteunrar
Source0:        chromium-%{version}-clean.tar.xz
%endif

# Patchset composed by Stephan Hartmann.
%global patchset_revision chromium-94-patchset-3
Source1:        https://github.com/stha09/chromium-patches/archive/%{patchset_revision}/chromium-patches-%{patchset_revision}.tar.gz

# The following two source files are copied and modified from the chromium source
Source10:       %{name}.sh
#Add our own appdata file.
Source11:       %{name}.appdata.xml
Source12:       chromium-symbolic.svg
#Personal stuff
Source15:       LICENSE
######################## Installation Folder #################################################
#Our installation folder
%global chromiumdir %{_libdir}/%{name}
########################################################################################
#Compiler settings
# Make sure we don't encounter any bug
BuildRequires:  clang
BuildRequires:  lld
BuildRequires:  llvm
# Basic tools and libraries needed for building
BuildRequires:  ninja-build, nodejs, bison, gperf, hwdata
BuildRequires:  libatomic
BuildRequires:  libcap-devel, cups-devel, alsa-lib-devel
BuildRequires:  mesa-libGL-devel, mesa-libEGL-devel
%if %{system_minizip}
BuildRequires:  minizip-compat-devel
%endif
# Pipewire need this.
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libexif), pkgconfig(nss)
BuildRequires:  pkgconfig(xtst), pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(dbus-1), pkgconfig(libudev)
BuildRequires:  pkgconfig(gnome-keyring-1)
BuildRequires:  pkgconfig(libffi)
#for vaapi
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
#BuildRequires:  /usr/bin/python2
BuildRequires:  /usr/bin/python3
BuildRequires:  python3-beautifulsoup4
BuildRequires:  python3-html5lib
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
%if %{system_re2}
BuildRequires:  re2-devel
%endif
# replace_gn_files.py --system-libraries
BuildRequires:  flac-devel
%if %{system_freetype}
BuildRequires:  freetype-devel
%endif
%if %{system_harfbuzz}
BuildRequires:  harfbuzz-devel
%endif
%if %{system_libicu}
BuildRequires:  libicu-devel
%endif
BuildRequires:  libdrm-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
# Chromium requires libvpx 1.5.0 and some non-default options
%if %{system_libvpx}
BuildRequires:  libvpx-devel
%endif
%if %{system_ffmpeg}
BuildRequires:  ffmpeg-devel
BuildRequires:  opus-devel
%endif
BuildRequires:  libwebp-devel
%if %{system_libxml2}
BuildRequires:  pkgconfig(libxml-2.0)
%endif
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  snappy-devel
BuildRequires:  expat-devel
BuildRequires:  pciutils-devel
BuildRequires:  speech-dispatcher-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libcurl-devel
BuildRequires:  libxshmfence-devel
# install desktop files
BuildRequires:  desktop-file-utils
# install AppData files
BuildRequires:  libappstream-glib
# Mojojojo need this >:(
BuildRequires:  java-1.8.0-openjdk-headless
# Libstdc++ static needed for linker
BuildRequires:  libstdc++-static
# Runtime Requirements
Requires:       hicolor-icon-theme
# GTK modules it expects to find for some reason.
Requires:       libcanberra-gtk3%{_isa}
# Make sure chromium-freeworld replaces chromium-vaapi
Provides:       chromium-vaapi = %{version}-%{release}
Obsoletes:      chromium-vaapi < %{version}-%{release}
#Some recommendations
Recommends:     libva-utils
%global debug_package %{nil}
# This build should be only available to amd64
ExclusiveArch:  x86_64 aarch64

# Gentoo patches:
Patch201:       chromium-93-EnumTable-crash.patch

# Arch Linux patches:
Patch226:      chromium-93-ffmpeg-4.4.patch
Patch1227:     chromium-94-ffmpeg-roll.patch
Patch1228:     add-a-TODO-about-a-missing-pnacl-flag.patch
Patch1229:     use-ffile-compilation-dir.patch

# Suse patches:
Patch231:      remove-llvm13-warning-flags.patch
Patch232:      chromium-91-sql-standard-layout-type.patch
Patch233:      chromium-clang-nomerge.patch

# Fedora patches:
Patch300:       chromium-py3-bootstrap.patch
Patch301:       chromium-gcc11.patch
Patch302:       chromium-py3-fixes.patch
Patch303:       chromium-java-only-allowed-in-android-builds.patch
Patch304:       chromium-aarch64-cxxflags-addition.patch
Patch305:       chromium-clang-format.patch
Patch1303:      chromium-rawhide-gcc-std-max-fix.patch

# RPM Fusion patches [free/chromium-freeworld]:
Patch400:       chromium-hw-accel-mjpeg.patch
Patch401:       chromium-fix-vaapi-on-intel.patch
Patch402:       chromium-enable-widevine.patch
Patch403:       chromium-manpage.patch
Patch404:       chromium-md5-based-build-id.patch
Patch405:       chromium-names.patch
Patch1406:      chromium-rpm-fusion-brand.patch

%description
%{name} is an open-source web browser, powered by WebKit (Blink)
############################################PREP###########################################################
%prep
%setup -q -T -n chromium-patches-%{patchset_revision} -b 1
%setup -q -n chromium-%{version}

%global patchset_root %{_builddir}/chromium-patches-%{patchset_revision}

# Apply patchset composed by Stephan Hartmann.
%global patchset_apply() \
  printf "Applying %%s\\n" %{1} \
  %{__scm_apply_patch -p1} <%{patchset_root}/%{1}

%patchset_apply chromium-78-protobuf-RepeatedPtrField-export.patch
%patchset_apply chromium-90-ruy-include.patch
%patchset_apply chromium-91-libyuv-aarch64.patch
%patchset_apply chromium-94-ConversionStorageSql-lambda.patch
%patchset_apply chromium-94-CustomSpaces-include.patch


# Apply patches up to #1000 from this spec.
%autopatch -M1000 -p1

# Manually apply patches that need an ifdef
%patch1227 -Rp1

%if 0%{?fedora} < 35
%patch1228 -Rp1
%patch1229 -Rp1
%endif

%if 0%{?fedora} >= 35
%patch1303 -p1
%endif

%if %{freeworld}
%patch1406 -p1
%endif

#Let's change the default shebang of python files.
find -type f -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' {} +
./build/linux/unbundle/remove_bundled_libraries.py --do-remove \
    base/third_party/cityhash \
    base/third_party/double_conversion \
    base/third_party/dynamic_annotations \
    base/third_party/icu \
    base/third_party/libevent \
    base/third_party/nspr \
    base/third_party/superfasthash \
    base/third_party/symbolize \
    base/third_party/valgrind \
    base/third_party/xdg_mime \
    base/third_party/xdg_user_dirs \
    buildtools/third_party/libc++ \
    buildtools/third_party/libc++abi \
    chrome/third_party/mozilla_security_manager \
    courgette/third_party \
    native_client/src/third_party/dlmalloc \
    native_client/src/third_party/valgrind \
    net/third_party/mozilla_security_manager \
    net/third_party/nss \
    net/third_party/quic \
    net/third_party/uri_template \
    third_party/abseil-cpp \
    third_party/angle \
    third_party/angle/src/common/third_party/base \
    third_party/angle/src/common/third_party/smhasher \
    third_party/angle/src/common/third_party/xxhash \
    third_party/angle/src/third_party/libXNVCtrl \
    third_party/angle/src/third_party/trace_event \
    third_party/angle/src/third_party/volk \
    third_party/libgifcodec \
    third_party/apple_apsl \
    third_party/axe-core \
    third_party/boringssl \
    third_party/boringssl/src/third_party/fiat \
    third_party/blink \
    third_party/breakpad \
    third_party/breakpad/breakpad/src/third_party/curl \
    third_party/brotli \
    third_party/catapult \
    third_party/catapult/common/py_vulcanize/third_party/rcssmin \
    third_party/catapult/common/py_vulcanize/third_party/rjsmin \
    third_party/catapult/third_party/beautifulsoup4 \
    third_party/catapult/third_party/html5lib-python \
    third_party/catapult/third_party/polymer \
    third_party/catapult/third_party/six \
    third_party/catapult/tracing/third_party/d3 \
    third_party/catapult/tracing/third_party/gl-matrix \
    third_party/catapult/tracing/third_party/jpeg-js \
    third_party/catapult/tracing/third_party/jszip \
    third_party/catapult/tracing/third_party/mannwhitneyu \
    third_party/catapult/tracing/third_party/oboe \
    third_party/catapult/tracing/third_party/pako \
    third_party/ced \
    third_party/cld_3 \
    third_party/closure_compiler \
    third_party/crashpad \
    third_party/crashpad/crashpad/third_party/lss \
    third_party/crashpad/crashpad/third_party/zlib \
    third_party/crc32c \
    third_party/cros_system_api \
    third_party/dawn \
    third_party/dawn/third_party/khronos \
    third_party/dawn/third_party/tint \
    third_party/depot_tools \
    third_party/dav1d \
    third_party/devscripts \
    third_party/devtools-frontend \
    third_party/devtools-frontend/src/front_end/third_party/acorn \
    third_party/devtools-frontend/src/front_end/third_party/axe-core \
    third_party/devtools-frontend/src/front_end/third_party/chromium \
    third_party/devtools-frontend/src/front_end/third_party/codemirror \
    third_party/devtools-frontend/src/front_end/third_party/diff \
    third_party/devtools-frontend/src/front_end/third_party/i18n \
    third_party/devtools-frontend/src/front_end/third_party/intl-messageformat \
    third_party/devtools-frontend/src/front_end/third_party/lighthouse \
    third_party/devtools-frontend/src/front_end/third_party/lit-html \
    third_party/devtools-frontend/src/front_end/third_party/lodash-isequal \
    third_party/devtools-frontend/src/front_end/third_party/marked \
    third_party/devtools-frontend/src/front_end/third_party/puppeteer \
    third_party/devtools-frontend/src/front_end/third_party/wasmparser \
    third_party/devtools-frontend/src/test/unittests/front_end/third_party/i18n \
    third_party/devtools-frontend/src/third_party \
    third_party/dom_distiller_js \
    third_party/eigen3 \
    third_party/emoji-segmenter \
    third_party/farmhash \
    third_party/fdlibm \
%if !%{system_ffmpeg}
    third_party/ffmpeg \
%endif
    third_party/fft2d \
    third_party/flatbuffers \
%if !%{system_freetype}
    third_party/freetype \
%endif
    third_party/fusejs \
    third_party/liburlpattern \
    third_party/libzip \
    third_party/gemmlowp \
    third_party/google_input_tools \
    third_party/google_input_tools/third_party/closure_library \
    third_party/google_input_tools/third_party/closure_library/third_party/closure \
    third_party/googletest \
%if !%{system_harfbuzz}
    third_party/harfbuzz-ng \
%endif
    third_party/harfbuzz-ng/utils \
    third_party/highway \
    third_party/hunspell \
    third_party/iccjpeg \
%if !%{system_libicu}
    third_party/icu \
%endif
    third_party/inspector_protocol \
    third_party/jinja2 \
    third_party/jsoncpp \
    third_party/jstemplate \
    third_party/khronos \
    third_party/leveldatabase \
    third_party/libaddressinput \
    third_party/libaom \
    third_party/libaom/source/libaom/third_party/fastfeat \
    third_party/libaom/source/libaom/third_party/vector \
    third_party/libaom/source/libaom/third_party/x86inc \
    third_party/libavif \
    third_party/libgav1 \
    third_party/libjingle \
    third_party/libjxl \
    third_party/libphonenumber \
    third_party/libsecret \
    third_party/libsrtp \
    third_party/libsync \
    third_party/libudev \
    third_party/libva_protected_content \
%if !%{system_libvpx}
    third_party/libvpx \
    third_party/libvpx/source/libvpx/third_party/x86inc \
%endif
    third_party/libwebm \
    third_party/libx11 \
    third_party/libxcb-keysyms \
%if %{system_libxml2}
    third_party/libxml/chromium \
%else
    third_party/libxml \
%endif
    third_party/libXNVCtrl \
    third_party/libyuv \
    third_party/lottie \
    third_party/lss \
    third_party/lzma_sdk \
    third_party/mako \
    third_party/markupsafe \
    third_party/mesa \
    third_party/metrics_proto \
    third_party/minigbm \
%if !%{system_minizip}
    third_party/minizip/ \
%endif
    third_party/modp_b64 \
    third_party/nasm \
    third_party/nearby \
    third_party/neon_2_sse \
    third_party/node \
    third_party/node/node_modules/polymer-bundler/lib/third_party/UglifyJS2 \
    third_party/one_euro_filter \
    third_party/opencv \
    third_party/openh264 \
    third_party/openscreen \
    third_party/openscreen/src/third_party/mozilla \
    third_party/openscreen/src/third_party/tinycbor/src/src \
    third_party/ots \
    third_party/pdfium \
    third_party/pdfium/third_party/agg23 \
    third_party/pdfium/third_party/base \
    third_party/pdfium/third_party/bigint \
    third_party/pdfium/third_party/freetype \
    third_party/pdfium/third_party/lcms \
    third_party/pdfium/third_party/libopenjpeg20 \
    third_party/pdfium/third_party/libpng16 \
    third_party/pdfium/third_party/libtiff \
    third_party/pdfium/third_party/skia_shared \
    third_party/perfetto \
    third_party/perfetto/protos/third_party/chromium \
    third_party/pffft \
    third_party/ply \
    third_party/polymer \
    third_party/private-join-and-compute \
    third_party/private_membership \
    third_party/protobuf \
    third_party/protobuf/third_party/six \
    third_party/pyjson5 \
    third_party/qcms \
%if !%{system_re2}
    third_party/re2 \
%endif
    third_party/rnnoise \
    third_party/ruy \
    third_party/s2cellid \
    third_party/securemessage \
    third_party/shell-encryption \
    third_party/skia \
    third_party/skia/include/third_party/skcms \
    third_party/skia/include/third_party/vulkan \
    third_party/skia/third_party/vulkan \
    third_party/skia/third_party/skcms \
    third_party/smhasher \
    third_party/speech-dispatcher \
    third_party/sqlite \
    third_party/swiftshader \
    third_party/swiftshader/third_party/astc-encoder \
    third_party/swiftshader/third_party/llvm-10.0 \
    third_party/swiftshader/third_party/llvm-subzero \
    third_party/swiftshader/third_party/marl \
    third_party/swiftshader/third_party/subzero \
    third_party/swiftshader/third_party/SPIRV-Headers/include/spirv/unified1 \
    third_party/tcmalloc \
    third_party/tensorflow-text \
    third_party/tflite \
    third_party/tflite/src/third_party/eigen3 \
    third_party/tflite/src/third_party/fft2d \
    third_party/tflite-support \
    third_party/ukey2 \
    third_party/unrar \
    third_party/utf \
    third_party/usb_ids \
    third_party/usrsctp \
    third_party/vulkan \
    third_party/wayland \
    third_party/web-animations-js \
    third_party/webdriver \
    third_party/webgpu-cts \
    third_party/webrtc \
    third_party/webrtc/common_audio/third_party/ooura \
    third_party/webrtc/common_audio/third_party/spl_sqrt_floor \
    third_party/webrtc/modules/third_party/fft \
    third_party/webrtc/modules/third_party/g711 \
    third_party/webrtc/modules/third_party/g722 \
    third_party/webrtc/rtc_base/third_party/base64 \
    third_party/webrtc/rtc_base/third_party/sigslot \
    third_party/widevine \
    third_party/woff2 \
    third_party/wuffs \
    third_party/x11proto \
    third_party/xcbproto \
    third_party/xdg-utils \
    third_party/zlib/google \
    third_party/zxcvbn-cpp \
%if !%{system_minizip}
    third_party/zlib \
%endif
    tools/gn/src/base/third_party/icu \
    url/third_party/mozilla \
    v8/src/third_party/siphash \
    v8/src/third_party/valgrind \
    v8/src/third_party/utf8-decoder \
    v8/third_party/inspector_protocol \
    v8/third_party/v8

# bundled eu-strip is for amd64 only and we don't want to pre-stripped binaries
mkdir -p buildtools/third_party/eu-strip/bin || die
ln -s %{_bindir}/true buildtools/third_party/eu-strip/bin/eu-strip || die

./build/linux/unbundle/replace_gn_files.py --system-libraries \
%if %{system_ffmpeg}
    ffmpeg \
    opus \
%endif
%if %{system_harfbuzz}
    harfbuzz-ng \
%endif
    flac \
%if %{system_freetype}
    freetype \
%endif
    fontconfig \
%if %{system_libicu}
    icu \
%endif
    libdrm \
    libjpeg \
    libpng \
%if %{system_libvpx}
    libvpx \
%endif
    libwebp \
%if %{system_libxml2}
    libxml \
%endif
    libxslt \
%if %{system_re2}
    re2 \
%endif
    snappy \
%if %{system_minizip}
    zlib
%endif

sed -i 's|//third_party/usb_ids|/usr/share/hwdata|g' \
    services/device/public/cpp/usb/BUILD.gn

# Allow building against system libraries in official builds
sed -i 's/OFFICIAL_BUILD/GOOGLE_CHROME_BUILD/' \
    tools/generate_shim_headers/generate_shim_headers.py || die

# Fix the path to nodejs binary
mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node
#####################################BUILD#############################################
%build
# Final link uses lots of file descriptors.
ulimit -n 2048

#export compilar variables
export CC=clang
export CXX=clang++
export AR=llvm-ar
export NM=llvm-nm
export CXXFLAGS="$CXXFLAGS -fpermissive"
export CFLAGS="$CFLAGS -w"
export CXXFLAGS="$CXXFLAGS -w"
export CFLAGS="$CFLAGS -g0"
export CXXFLAGS="$CXXFLAGS -g0"

gn_args=(
    'rpm_fusion_package_name="%{name}"'
    'rpm_fusion_menu_name="%{menu_name}"'
    is_debug=false
    use_vaapi=true
    is_component_build=false
    is_official_build=true
    use_sysroot=false
    use_custom_libcxx=false
    use_aura=true
    'system_libdir="%{_lib}"'
    use_cups=true
    use_gnome_keyring=true
    use_gio=true
    use_gold=false
    use_kerberos=true
    use_libpci=true
    use_pulseaudio=true
    link_pulseaudio=true
%if %{system_freetype}
    use_system_freetype=true
%endif
    enable_widevine=true
%if %{system_harfbuzz}
    use_system_harfbuzz=true
%endif
%if %{freeworld}
    'ffmpeg_branding="Chrome"'
    proprietary_codecs=true
%else
    'ffmpeg_branding="Chromium"'
    proprietary_codecs=false
%endif
    enable_nacl=false
%if 0%{?fedora} < 34
    chrome_pgo_phase=0
%endif
    enable_hangout_services_extension=true
    fatal_linker_warnings=false
    treat_warnings_as_errors=false
    disable_fieldtrial_testing_config=true
    'custom_toolchain="//build/toolchain/linux/unbundle:default"'
    'host_toolchain="//build/toolchain/linux/unbundle:default"'
    'google_api_key="%{api_key}"'
)

# Optimizations
gn_args+=(
   enable_vr=false
%if %{system_libicu}
   icu_use_data_file=false
%endif
)


gn_args+=(
    is_clang=true
    clang_use_chrome_plugins=false
    use_thin_lto=false
    use_lld=false
    is_cfi=false
)

#Pipewire
gn_args+=(
     rtc_use_pipewire=true
     rtc_link_pipewire=true
)

#symbol
gn_args+=(
    symbol_level=0
    blink_symbol_level=0
)

tools/gn/bootstrap/bootstrap.py  --gn-gen-args "${gn_args[*]}"
%{target}/gn --script-executable=%{__python3} gen --args="${gn_args[*]}" %{target}
%ninja_build -C %{target} chrome chrome_sandbox chromedriver
######################################Install####################################
%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromiumdir}/locales
mkdir -p %{buildroot}%{chromiumdir}/MEIPreload
mkdir -p %{buildroot}%{chromiumdir}/swiftshader
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_metainfodir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps
sed -e "s|@@CHROMIUMDIR@@|%{chromiumdir}|"     %{SOURCE10} > %{name}.sh
install -m 755 %{name}.sh %{buildroot}%{_bindir}/%{name}
install -m 644 %{SOURCE11} %{buildroot}%{_metainfodir}
sed \
  -e "s|@@MENUNAME@@|Chromium|g" \
  -e "s|@@PACKAGE@@|%{name}|g" \
  -e "s|@@SUMMARY@@|%{summary}|g" \
  -e "s|@@XDG_SUBDIR@@|%{xdg_subdir}|g" \
  chrome/app/resources/manpage.1.in >chrome.1
install -m 644 chrome.1 %{buildroot}%{_mandir}/man1/%{name}.1
sed \
  -e "s|@@MENUNAME@@|%{menu_name}|g" \
  -e "s|@@PACKAGE@@|%{name}|g" \
  -e "s|@@USR_BIN_SYMLINK_NAME@@|%{name}|g" \
  chrome/installer/linux/common/desktop.template >%{name}.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{name}.desktop
sed \
  -e "s|@@INSTALLDIR@@|%{_bindir}|g" \
  -e "s|@@MENUNAME@@|%{menu_name}|g" \
  -e "s|@@PACKAGE@@|%{name}|g" \
  chrome/installer/linux/common/default-app.template >%{name}.xml
install -m 644 %{name}.xml %{buildroot}%{_datadir}/gnome-control-center/default-apps/
install -m 755 %{target}/chrome %{buildroot}%{chromiumdir}/%{name}
install -m 4755 %{target}/chrome_sandbox %{buildroot}%{chromiumdir}/chrome-sandbox
mv %{target}/chromedriver{.unstripped,} || die
install -m 755 %{target}/chromedriver %{buildroot}%{chromiumdir}/
install -m 755 %{target}/chrome_crashpad_handler %{buildroot}%{chromiumdir}/
install -m 755 %{target}/libEGL.so %{buildroot}%{chromiumdir}/
install -m 755 %{target}/libGLESv2.so %{buildroot}%{chromiumdir}/
%if !%{system_libicu}
install -m 644 %{target}/icudtl.dat %{buildroot}%{chromiumdir}/
%endif
install -m 644 %{target}/v8_context_snapshot.bin %{buildroot}%{chromiumdir}/
install -m 644 %{target}/*.pak %{buildroot}%{chromiumdir}/
install -m 644 %{target}/locales/*.pak %{buildroot}%{chromiumdir}/locales/
install -m 644 %{target}/xdg*  %{buildroot}%{chromiumdir}/
install -m 644 %{target}/MEIPreload/* %{buildroot}%{chromiumdir}/MEIPreload/
install -m 755 %{target}/swiftshader/*.so %{buildroot}%{chromiumdir}/swiftshader/

# Icons
for i in 16 32; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/default_100_percent/chromium/product_logo_$i.png \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done
for i in 24 32 48 64 128 256; do
    if [ ${i} = 32 ]; then ext=xpm; else ext=png; fi
    if [ ${i} = 32 ]; then dir=linux/; else dir=; fi
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/chromium/${dir}product_logo_$i.${ext} \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.${ext}
done
install -m 644 %{SOURCE12} \
  %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps/%{name}-symbolic.svg
####################################check##################################################
%check
appstream-util validate-relax --nonet "%{buildroot}%{_metainfodir}/%{name}.appdata.xml"
######################################files################################################
%files
%license LICENSE
%doc AUTHORS
%{_bindir}/%{name}
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome-control-center/default-apps/%{name}.xml
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.xpm
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/symbolic/apps/%{name}-symbolic.svg
%{_mandir}/man1/%{name}.1.*
%dir %{chromiumdir}
%{chromiumdir}/%{name}
%{chromiumdir}/chrome-sandbox
%{chromiumdir}/chromedriver
%{chromiumdir}/chrome_crashpad_handler
%{chromiumdir}/libEGL.so
%{chromiumdir}/libGLESv2.so
%if !%{system_libicu}
%{chromiumdir}/icudtl.dat
%endif
%{chromiumdir}/v8_context_snapshot.bin
%{chromiumdir}/*.pak
%{chromiumdir}/xdg-mime
%{chromiumdir}/xdg-settings
%dir %{chromiumdir}/MEIPreload
%{chromiumdir}/MEIPreload/manifest.json
%{chromiumdir}/MEIPreload/preloaded_data.pb
%dir %{chromiumdir}/locales
%{chromiumdir}/locales/*.pak
%dir %{chromiumdir}/swiftshader
%{chromiumdir}/swiftshader/libEGL.so
%{chromiumdir}/swiftshader/libGLESv2.so
#########################################changelogs#################################################
%changelog
* Wed Sep 22 2021 Leigh Scott <leigh123linux@gmail.com> - 94.0.4606.61-1
- Update to 94.0.4606.61

* Tue Sep 14 2021 Leigh Scott <leigh123linux@gmail.com> - 93.0.4577.82-1
- Update to 93.0.4577.82

* Sat Sep 11 2021 Leigh Scott <leigh123linux@gmail.com> - 93.0.4577.63-3
- Use clang to compile

* Fri Sep 03 2021 Leigh Scott <leigh123linux@gmail.com> - 93.0.4577.63-2
- Enable aarch64 build

* Wed Sep 01 2021 Leigh Scott <leigh123linux@gmail.com> - 93.0.4577.63-1
- Update to 93.0.4577.63

* Tue Aug 31 2021 Leigh Scott <leigh123linux@gmail.com> - 92.0.4515.166-1
- Update to 92.0.4515.166

* Thu Aug 26 2021 Leigh Scott <leigh123linux@gmail.com> - 92.0.4515.159-5
- Enable expired vaapi support

* Wed Aug 25 2021 Leigh Scott <leigh123linux@gmail.com> - 92.0.4515.159-4
- Disable eu-strip

* Sun Aug 22 2021 Leigh Scott <leigh123linux@gmail.com> - 92.0.4515.159-3
- Fix sandbox crash

* Sun Aug 22 2021 Leigh Scott <leigh123linux@gmail.com> - 92.0.4515.159-2
- Add missing file and add crashpad_handler consent patch

* Sat Aug 21 2021 Leigh Scott <leigh123linux@gmail.com> - 92.0.4515.159-1
- Update to 92.0.4515.159

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 90.0.4430.85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Apr 22 2021 qvint <dotqvint@gmail.com> - 90.0.4430.85-1
- Update to 90.0.4430.85

* Sat Apr 17 2021 Leigh Scott <leigh123linux@gmail.com> - 89.0.4389.114-2
- Rebuild for F33 to include missed patches (rfbz#5973)

* Sun Apr 04 2021 qvint <dotqvint@gmail.com> - 89.0.4389.114-1
- Update to 89.0.4389.114

* Thu Feb 04 2021 qvint <dotqvint@gmail.com> - 88.0.4324.150-1
- Update to 88.0.4324.150

* Wed Jan 20 2021 qvint <dotqvint@gmail.com> - 88.0.4324.96-1
- Update to 88.0.4324.96
- Comply with new Google API key rules for derivatives
- Fix Icon key in chrome-apps.directory (rfbz#5895)
- Fix PulseAudio application name and icon
- Don't depend on CHROME_DESKTOP env var
- Sync shell wrapper with Fedora Chromium (rfbz#5859, rhbz#1902983)

* Tue Dec 08 2020 qvint <dotqvint@gmail.com> - 87.0.4280.88-1
- Update to 87.0.4280.88

* Fri Nov 27 2020 qvint <dotqvint@gmail.com> - 87.0.4280.66-1
- Update to 87.0.4280.66

* Tue Oct 27 2020 qvint <dotqvint@gmail.com> - 86.0.4240.111-2
- Fix invalid "end" iterator usage in CookieMonster
- Only fall back to the i965 driver if we're on iHD
- Check for enable-accelerated-video-decode
- Fix mouse movements near window edges
- Fix crash in UserInputMonitorLinuxCore (rfbz#5807)

* Wed Oct 21 2020 qvint <dotqvint@gmail.com> - 86.0.4240.111-1
- Update to 86.0.4240.111

* Wed Sep 23 2020 qvint <dotqvint@gmail.com> - 85.0.4183.121-1
- Update to 85.0.4183.121
- Enable Hangout services extension (rfbz#5758)
- Use MD5-based BuildID (rfbz#5743)
- Use %%ninja_build macro
- Remove debug_pkg toggle
- Replace bconds with ordinary macros
- Use system re2
- Use system libicu (f33+)

* Thu Sep 10 2020 qvint <dotqvint@gmail.com> - 85.0.4183.102-1
- Update to 85.0.4183.102
- Remove bundlepylibs and clang toggles

* Mon Aug 31 2020 qvint <dotqvint@gmail.com> - 85.0.4183.83-2
- Ship ANGLE libEGL.so and libGLESv2.so (rfbz#5738)

* Wed Aug 26 2020 qvint <dotqvint@gmail.com> - 85.0.4183.83-1
- Update to 85.0.4183.83
- Use xcb-proto bundled in Chromium tarball
- Drop Fedora 30 support
- Fix XDG paths in manpage
- Update AppStream metadata
- Fix name in .desktop file (rfbz#5717)
- Fix name in GNOME default-apps XML
- Add symbolic app icon

* Tue Aug 11 2020 qvint <dotqvint@gmail.com> - 84.0.4147.125-1
- Update to 84.0.4147.125
- Stop using gold
- Add 'ulimit -n 2048'

* Sat Jul 18 2020 qvint <dotqvint@gmail.com> - 84.0.4147.89-1
- Update to 84.0.4147.89
- Use patchset composed by Stephan Hartmann <stha09@googlemail.com>
- Bundle xcb-proto

* Thu Jun 25 2020 qvint <dotqvint@gmail.com> - 83.0.4103.116-1
- Update to 83.0.4103.116

* Wed Jun 17 2020 qvint <dotqvint@gmail.com> - 83.0.4103.106-1
- Update to 83.0.4103.106
- Disable python byte compiling

* Mon Jun 08 2020 qvint <dotqvint@gmail.com> - 83.0.4103.97-2
- Fix crash in ServiceWorker (rfbz#5671)

* Fri Jun 05 2020 qvint <dotqvint@gmail.com> - 83.0.4103.97-1
- Update to 83.0.4103.97

* Wed May 06 2020 qvint <dotqvint@gmail.com> - 81.0.4044.138-1
- Update to 81.0.4044.138
- Fix touchpad scrolling under XWayland (rfbz#5621)

* Thu Apr 30 2020 qvint <dotqvint@gmail.com> - 81.0.4044.129-1
- Update to 81.0.4044.129

* Thu Apr 09 2020 qvint <dotqvint@gmail.com> - 81.0.4044.92-1
- Update to 81.0.4044.92

* Sun Apr 05 2020 qvint <dotqvint@gmail.com> - 80.0.3987.163-1
- Update to 80.0.3987.163

* Thu Apr 02 2020 qvint <dotqvint@gmail.com> - 80.0.3987.162-1
- Update to 80.0.3987.162

* Wed Mar 18 2020 qvint <dotqvint@gmail.com> - 80.0.3987.149-1
- Update to 80.0.3987.149
- Fix rpmlint warnings and errors

* Wed Mar 04 2020 qvint <dotqvint@gmail.com> - 80.0.3987.132-1
- Update to 80.0.3987.132

* Sun Mar 01 2020 qvint <dotqvint@gmail.com> - 80.0.3987.122-1
- Update to 80.0.3987.122

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 79.0.3945.130-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Vasiliy Glazov <vascom2@gmail.com> - 79.0.3945.130-1
- Update to 79.0.3945.130

* Tue Jan 14 2020 Vasiliy Glazov <vascom2@gmail.com> - 79.0.3945.117-1
- Update to 79.0.3945.117

* Sat Dec 21 2019 Akarshan Biswas <akarshanbiswas@fedoraproject.org> - 79.0.3945.88-1
- Update to 79.0.3945.88

* Fri Dec 13 2019 Akarshan Biswas <akarshanbiswas@fedoraproject.org> - 79.0.3945.79-1
- Update to 79.0.3945.79

* Fri Dec 06 2019 Vasiliy Glazov <vascom2@gmail.com> - 78.0.3904.108-2
- Disable fedora's build flags to reduce binary size

* Thu Nov 21 2019 Vasiliy Glazov <vascom2@gmail.com> - 78.0.3904.108-1
- Update to 78.0.3904.108

* Tue Nov 12 2019 Vasiliy Glazov <vascom2@gmail.com> - 78.0.3904.97-1
- Update to 78.0.3904.97

* Sat Nov 02 2019 Akarshan Biswas <akarshanbiswas@fedoraproject.org> - 78.0.3904.87-1
- Update to 78.0.3904.87

* Thu Oct 31 2019 Akarshan Biswas <akarshanbiswas@fedoraproject.org> - 78.0.3904.70-1
- IMPORT: rename package; add back Fedora build flags
