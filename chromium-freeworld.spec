#Global Libraries
%global menu_name Chromium (Freeworld)
%global xdg_subdir chromium
%ifarch aarch64
%global _smp_build_ncpus 6
%endif
%undefine _auto_set_build_flags
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
%global system_libdrm 1
# Chrome upstream uses custom ffmpeg patches
%global system_ffmpeg 0
%global system_flac 1
%global system_fontconfig 1
# fedora freetype is too old
%global system_freetype 0
%global system_harfbuzz 0
%global system_libjpeg 1
%global system_libicu 0
# lto issue with system libpng
%global system_libpng 0
%global system_libvpx 0
%global system_libxml2 0
# lto issue with system minizip
%global system_minizip 0
%global system_re2 1
%global system_libwebp 1
%global system_xslt 1

##############################Package Definitions######################################
Name:           chromium-freeworld
Version:        99.0.4844.51
Release:        1%{?dist}
Summary:        Chromium built with all freeworld codecs and VA-API support
License:        BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:            https://www.chromium.org/Home
Source0:        https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz

# Patchset composed by Stephan Hartmann.
%global patchset_revision chromium-99-patchset-3
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
BuildRequires:  clang, clang-tools-extra
BuildRequires:  lld
BuildRequires:  llvm
# Basic tools and libraries needed for building
BuildRequires:  ninja-build, nodejs, bison, gperf, hwdata
BuildRequires:  libatomic, flex, perl-Switch
BuildRequires:  libcap-devel, cups-devel, alsa-lib-devel
BuildRequires:  mesa-libGL-devel, mesa-libEGL-devel
# Pipewire need this.
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libexif), pkgconfig(nss)
BuildRequires:  pkgconfig(xtst), pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(dbus-1), pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(libudev), pkgconfig(uuid)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xcb-proto)
BuildRequires:  pkgconfig(gnome-keyring-1)
BuildRequires:  pkgconfig(libffi)
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
# Libstdc++ static needed for linker
BuildRequires:  libstdc++-static
#for vaapi
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)

BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command
BuildRequires:  python3-beautifulsoup4
BuildRequires:  python3-html5lib
BuildRequires:  python3-json5
BuildRequires:  python3-mako
BuildRequires:  python3-markupsafe
BuildRequires:  python3-ply
BuildRequires:  python3-simplejson
BuildRequires:  python3-six
# replace_gn_files.py --system-libraries
%if %{system_flac}
BuildRequires:  flac-devel
%endif
%if %{system_freetype}
BuildRequires:  freetype-devel
%endif
%if %{system_harfbuzz}
BuildRequires:  harfbuzz-devel
%endif
%if %{system_libicu}
BuildRequires:  libicu-devel
%endif
%if %{system_libdrm}
BuildRequires:  libdrm-devel
%endif
%if %{system_libjpeg}
BuildRequires:  libjpeg-turbo-devel
%endif
%if %{system_libpng}
BuildRequires:  libpng-devel
%endif
%if %{system_libvpx}
BuildRequires:  libvpx-devel
%endif
%if %{system_ffmpeg}
%if 0%{?fedora} && 0%{?fedora} > 35
BuildRequires:  compat-ffmpeg4-devel
%else
BuildRequires:  ffmpeg-devel
%endif
BuildRequires:  opus-devel
%endif
%if %{system_libwebp}
BuildRequires:  libwebp-devel
%endif
%if %{system_minizip}
BuildRequires:  minizip-compat-devel
%endif
%if %{system_libxml2}
BuildRequires:  pkgconfig(libxml-2.0)
%endif
%if %{system_xslt}
BuildRequires:  pkgconfig(libxslt)
%endif
%if %{system_re2}
BuildRequires:  re2-devel
%endif

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
Patch201:       chromium-98-EnumTable-crash.patch
Patch202:       chromium-InkDropHost-crash.patch
Patch203:       chromium-98-system-libdrm.patch
Patch1204:      chromium-glibc-2.34-r1.patch

# Arch Linux patches:
Patch220:       webcodecs-stop-using-AudioOpusEncoder.patch
Patch1226:      chromium-93-ffmpeg-4.4.patch
Patch1227:      unbundle-ffmpeg-av_stream_get_first_dts.patch
Patch1228:      add-a-TODO-about-a-missing-pnacl-flag.patch
Patch1229:      use-ffile-compilation-dir.patch

# Suse patches:
Patch232:       chromium-91-sql-standard-layout-type.patch
Patch233:       chromium-clang-nomerge.patch

# Fedora patches:
Patch300:       chromium-py3-bootstrap.patch
Patch301:       chromium-gcc11.patch
Patch302:       chromium-java-only-allowed-in-android-builds.patch
Patch303:       chromium-aarch64-cxxflags-addition.patch
# Causes build error
#Patch304:       chromium-clang-format.patch

# RPM Fusion patches [free/chromium-freeworld]:
Patch401:       chromium-fix-vaapi-on-intel.patch
Patch402:       chromium-enable-widevine.patch
Patch403:       chromium-manpage.patch
Patch404:       chromium-md5-based-build-id.patch
Patch405:       chromium-names.patch
Patch406:       gcc12.patch
Patch407:       allow-to-override-clang-through-env-variables.patch
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
%patchset_apply chromium-99-AutofillAssistantModelExecutor-NoDestructor.patch


# Apply patches up to #1000 from this spec.
%autopatch -M1000 -p1

# Manually apply patches that need an ifdef
%if 0%{?fedora} >= 35
%patch1204 -p1
%endif

%if %{system_ffmpeg}
%patch1226 -p1
%patch1227 -p1
%endif

%if 0%{?fedora} < 35
%patch1228 -Rp1
%patch1229 -Rp1
%endif

%patch1406 -p1

./build/linux/unbundle/replace_gn_files.py --system-libraries \
%if %{system_ffmpeg}
    ffmpeg \
    opus \
%endif
%if %{system_harfbuzz}
    harfbuzz-ng \
%endif
%if %{system_flac}
    flac \
%endif
%if %{system_freetype}
    freetype \
%endif
%if %{system_fontconfig}
    fontconfig \
%endif
%if %{system_libicu}
    icu \
%endif
%if %{system_libdrm}
    libdrm \
%endif
%if %{system_libjpeg}
    libjpeg \
%endif
%if %{system_libpng}
    libpng \
%endif
%if %{system_libvpx}
    libvpx \
%endif
%if %{system_libwebp}
    libwebp \
%endif
%if %{system_libxml2}
    libxml \
%endif
%if %{system_xslt}
    libxslt \
%endif
%if %{system_re2}
    re2 \
%endif
%if %{system_minizip}
    zlib
%endif

# Too much debuginfo
sed -i 's|-g2|-g0|g' build/config/compiler/BUILD.gn

sed -i 's|//third_party/usb_ids|/usr/share/hwdata|g' \
    services/device/public/cpp/usb/BUILD.gn

sed -i \
	-e 's/"-ffile-compilation-dir=."//g' \
	-e 's/"-no-canonical-prefixes"//g' \
	build/config/compiler/BUILD.gn

mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node

mkdir -p buildtools/third_party/eu-strip/bin
ln -sf %{_bindir}/strip buildtools/third_party/eu-strip/bin/eu-strip

rm -f -- third_party/depot_tools/ninja
ln -s %{_bindir}/ninja third_party/depot_tools/ninja
ln -s %{_bindir}/python3 third_party/depot_tools/python

%build
%if 0%{?fedora} && 0%{?fedora} > 35
export PKG_CONFIG_PATH="%{_libdir}/compat-ffmpeg4/pkgconfig"
%endif
# Final link uses lots of file descriptors.
ulimit -n 2048

#export compilar variables
export CC="clang"
export CXX="clang++"
export AR="llvm-ar"
export NM="llvm-nm"
export READELF="llvm-readelf"

export RANLIB="ranlib"
export PATH="$PWD/third_party/depot_tools:$PATH"
export CHROMIUM_RPATH="%{_libdir}/%{name}"

FLAGS='-Wno-unknown-warning-option'

export CFLAGS="$FLAGS"
export CXXFLAGS="$FLAGS"

CHROMIUM_GN_DEFINES=
gn_arg() { CHROMIUM_GN_DEFINES="$CHROMIUM_GN_DEFINES $*"; }

gn_arg 'rpm_fusion_package_name="%{name}"'
gn_arg 'rpm_fusion_menu_name="%{menu_name}"'
gn_arg custom_toolchain=\"//build/toolchain/linux/unbundle:default\"
gn_arg host_toolchain=\"//build/toolchain/linux/unbundle:default\"
gn_arg is_official_build=true
gn_arg disable_fieldtrial_testing_config=true
gn_arg use_custom_libcxx=false
gn_arg use_sysroot=false
gn_arg use_gio=true
gn_arg use_glib=true
gn_arg use_libpci=true
gn_arg use_pulseaudio=true
gn_arg use_aura=true
gn_arg use_cups=true
gn_arg use_kerberos=true
gn_arg use_gold=false
gn_arg use_vaapi=true
gn_arg optimize_webui=false
%if %{system_freetype}
gn_arg use_system_freetype=true
%endif
%if %{system_harfbuzz}
gn_arg use_system_harfbuzz=true
%endif
gn_arg link_pulseaudio=true
gn_arg enable_hangout_services_extension=true
gn_arg treat_warnings_as_errors=false
gn_arg fatal_linker_warnings=false
gn_arg system_libdir=\"%{_lib}\"
gn_arg use_allocator=\"none\"
gn_arg use_icf=false
gn_arg enable_js_type_check=false
gn_arg use_system_libwayland=true
gn_arg use_system_wayland_scanner=true
gn_arg use_bundled_weston=false

%ifarch aarch64
gn_arg 'target_cpu="arm64"'
%endif

# ffmpeg
gn_arg ffmpeg_branding=\"Chrome\"
gn_arg proprietary_codecs=true

# Remove debug
gn_arg is_debug=false
gn_arg symbol_level=0

gn_arg enable_nacl=false
gn_arg is_component_build=false
gn_arg enable_widevine=true

gn_arg rtc_use_pipewire=true
gn_arg rtc_link_pipewire=true

gn_arg clang_base_path=\"%{_prefix}\"
gn_arg is_clang=true
gn_arg clang_use_chrome_plugins=false
gn_arg use_lld=true
gn_arg use_thin_lto=true
gn_arg is_cfi=false
gn_arg use_cfi_icall=false
gn_arg chrome_pgo_phase=0

%if %{system_libicu}
gn_arg icu_use_data_file=false
%endif

gn_arg enable_vulkan=true

gn_arg 'google_api_key="%{api_key}"'


tools/gn/bootstrap/bootstrap.py --gn-gen-args="$CHROMIUM_GN_DEFINES" --build-path=%{target}
%{target}/gn --script-executable=%{__python3} gen --args="$CHROMIUM_GN_DEFINES" %{target}
%ninja_build -C %{target} chrome chrome_sandbox
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
install -m 755 %{target}/chrome_crashpad_handler %{buildroot}%{chromiumdir}/
install -m 755 %{target}/libEGL.so %{buildroot}%{chromiumdir}/
install -m 755 %{target}/libGLESv2.so %{buildroot}%{chromiumdir}/
%if !%{system_libicu}
install -m 644 %{target}/icudtl.dat %{buildroot}%{chromiumdir}/
%endif
install -m 644 %{target}/v8_context_snapshot.bin %{buildroot}%{chromiumdir}/
install -m 644 %{target}/snapshot_blob.bin %{buildroot}%{chromiumdir}/
install -m 644 %{target}/*.pak %{buildroot}%{chromiumdir}/
install -m 644 %{target}/locales/*.pak %{buildroot}%{chromiumdir}/locales/
install -m 755 %{target}/xdg*  %{buildroot}%{chromiumdir}/
install -m 644 %{target}/MEIPreload/* %{buildroot}%{chromiumdir}/MEIPreload/
install -m 755 %{target}/swiftshader/*.so %{buildroot}%{chromiumdir}/swiftshader/
install -m 755 %{target}/libvk_swiftshader.so %{buildroot}%{chromiumdir}/
install -m 755 %{target}/libvulkan.so.1 %{buildroot}%{chromiumdir}/
install -m 644 %{target}/vk_swiftshader_icd.json %{buildroot}%{chromiumdir}/

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
%{chromiumdir}/chrome_crashpad_handler
%{chromiumdir}/libEGL.so
%{chromiumdir}/libGLESv2.so
%if !%{system_libicu}
%{chromiumdir}/icudtl.dat
%endif
%{chromiumdir}/v8_context_snapshot.bin
%{chromiumdir}/snapshot_blob.bin
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
%{chromiumdir}/libvk_swiftshader.so*
%{chromiumdir}/libvulkan.so*
%{chromiumdir}/vk_swiftshader_icd.json
#########################################changelogs#################################################
%changelog
* Wed Mar 02 2022 Leigh Scott <leigh123linux@gmail.com> - 99.0.4844.51-1
- Update to 99.0.4844.51

* Sat Feb 19 2022 Leigh Scott <leigh123linux@gmail.com> - 98.0.4758.102-2
- Use compat-ffmpeg4 for f36+

* Thu Feb 17 2022 Leigh Scott <leigh123linux@gmail.com> - 98.0.4758.102-1
- Update to 98.0.4758.102

* Wed Feb 02 2022 Leigh Scott <leigh123linux@gmail.com> - 98.0.4758.80-1
- Update to 98.0.4758.80

* Thu Jan 20 2022 Leigh Scott <leigh123linux@gmail.com> - 97.0.4692.99-1
- Update to 97.0.4692.99

* Wed Jan 05 2022 Leigh Scott <leigh123linux@gmail.com> - 97.0.4692.71-1
- Update to 97.0.4692.71

* Tue Dec 14 2021 Leigh Scott <leigh123linux@gmail.com> - 96.0.4664.110-1
- Update to 96.0.4664.110

* Tue Dec 07 2021 Leigh Scott <leigh123linux@gmail.com> - 96.0.4664.93-1
- Update to 96.0.4664.93

* Mon Nov 15 2021 Leigh Scott <leigh123linux@gmail.com> - 96.0.4664.45-1
- Update to 96.0.4664.45

* Tue Nov 09 2021 Leigh Scott <leigh123linux@gmail.com> - 95.0.4638.69-2
- Rebuilt for new ffmpeg snapshot

* Fri Oct 29 2021 Leigh Scott <leigh123linux@gmail.com> - 95.0.4638.69-1
- Update to 95.0.4638.69

* Tue Oct 19 2021 Leigh Scott <leigh123linux@gmail.com> - 95.0.4638.54-1
- Update to 95.0.4638.54

* Thu Oct 07 2021 Leigh Scott <leigh123linux@gmail.com> - 94.0.4606.81-1
- Update to 94.0.4606.81

* Thu Sep 30 2021 Leigh Scott <leigh123linux@gmail.com> - 94.0.4606.71-1
- Update to 94.0.4606.71

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

