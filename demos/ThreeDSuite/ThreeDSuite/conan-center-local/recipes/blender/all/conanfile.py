from conan import ConanFile
from conan.tools.files import apply_conandata_patches, export_conandata_patches, chdir, copy, export_conandata_patches, get, save
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.layout import basic_layout
from conan.tools.microsoft import is_msvc, VCVars
from conan.tools.system.package_manager import Apt, Yum, PacMan, Zypper
import os

required_conan_version = ">=1.53.0"

class BlenderConan(ConanFile):
    name = "blender"
    description = (
        "Blender is the free and open source 3D creation suite. \
         It supports the entirety of the 3D pipeline—modeling, rigging, \
         animation, simulation, rendering, compositing, motion tracking \
         and video editing."
    )
    topics = ("blender", "3D", "Creation")
    homepage = "https://www.blender.org/"
    url = "https://projects.blender.org/blender/blender"
    
    # https://www.blender.org/about/license/
    license = "GPL-3.0-or-later"
    settings = "os", "arch", "compiler", "build_type"

    options = {
        "install_prefix": [None, "ANY"],
    }
    default_options = {
        "install_prefix": None,
    }

    def system_requirements(self):
        # depending on the platform or the tools.system.package_manager:tool configuration
        # only one of these will be executed
#        Apt(self).install([])
        Yum(self).install([
            "libjpeg-turbo-devel",
            "libpng-devel",
            "libzstd-devel",
            "libepoxy-devel",
            "vulkan-headers",
            "vulkan-loader-devel",
            "libshaderc-devel",
            "freetype-devel",
            "libtiff-devel",

# libfontenc-devel libXdmcp-devel libxkbfile-devel libXres-devel xcb-util-wm-devel xcb-util-keysyms-devel libXxf86vm-devel xcb-util-devel

#        "mesa-libGL-devel",
#        "mesa-libEGL-devel",
#        "libX11-devel",
#        "libXxf86vm-devel",
#        "libXi-devel",
#        "libXcursor-devel",
#        "libXrandr-devel",
#        "libXinerama-devel",
#
#        "wayland-devel",
#        "wayland-protocols-devel",
#        "libxkbcommon-devel",
#        "dbus-devel",
#        "kernel-headers",
#
#        "patch",
#        "libdecor-devel",
#
#        "fontconfig",
#        "bzip2-devel",
#        "lzma-sdk-devel",
#        "SDL2-devel",
#        "libxml2-devel",
#        "libharu-devel",
#        "pystring-devel",
#        "openjpeg2-devel",
#        "jack-audio-connection-kit-devel",
#        "pulseaudio-libs-devel",
#        "pipewire-devel",
#        "openal-soft-devel",
#        "libsndfile-devel",
#        "jemalloc-devel",
#
#
#        "gmp-devel",
#        "pugixml-devel",
#        "fftw-devel",
#        "potrace-devel",
#        "yaml-cpp-devel",
#
#        "libdeflate-devel",
#
#        "python3-devel",
#        "python3-Cython",
#        "python3-idna",
#        "python3-charset-normalizer",
#        "python3-urllib3",
#        "python3-certifi",
#        "python3-requests",
#        "python3-zstandard",
#        "python3-numpy",
#
#        "tbb-devel",
#        "OpenColorIO-devel",
#        "imath-devel",
#        "openexr-devel",
#
#        "OpenImageIO-utils",
#        "OpenImageIO-devel",
#
#        "clang",  # clang-format is part of the main clang package.
#        "clang-devel",
#        "llvm-devel",
#        "openshadinglanguage-devel",
#        "opensubdiv-devel",
#
#        "blosc-devel",
#
#        "openvdb-devel",
#        "alembic-devel",
#
#        "usd-devel",
#        "openCOLLADA-devel",
#        "embree-devel",
#        "oidn-devel",
#        "oneapi-level-zero-devel",
#        "openpgl-devel",
#
#        "ffmpeg-free-devel",
#        "harfbuzz-devel",
        ])

# git git-lfs subversion ninja-build cmake-gui
# yum install --enablerepo crb -y libshaderc-devel


# python version
#
#  'PYTHON_VERSION=3.11' not found! This is the only officially supported
#  version.  If you wish to use a newer Python version you may set
#  'PYTHON_VERSION' however we do not guarantee full compatibility in this
#  case.  (missing: PYTHON_LIBRARY PYTHON_LIBPATH PYTHON_INCLUDE_DIR
#  PYTHON_INCLUDE_CONFIG_DIR)

#    PacMan(self).install([])
#    Zypper(self).install([])

# Basic mandatory set of common libraries to build Blender, which are also available as pre-conmpiled libraries.

# https://developer.blender.org/docs/handbook/building_blender/linux/#__tabbed_1_3

# ./build_files/build_environment/install_linux_packages.py

#BUILD_OPTIONAL_SUBPACKAGES = (
#    Package(name="Ninja Builder",
#            distro_package_names={DISTRO_ID_DEBIAN: "ninja-build",
#                                  DISTRO_ID_FEDORA: "ninja-build",
#                                  DISTRO_ID_SUSE: "ninja",
#                                  DISTRO_ID_ARCH: "ninja",
#                                  },
#            ),
# ./build_files/build_environment/linux/linux_rocky8_setup.sh
# make release


    def requirements(self):
        self.requires("cpython/3.11.9")

#        self.requires("mpfr/4.2.0")
#        self.requires("gmp/6.3.0")
#        self.requires("zlib/[>=1.2.13 <2]")
#        self.requires("isl/0.26")

    @property
    def _settings_build(self):
        return getattr(self, "settings_build", self.settings)

    def export_sources(self):
        export_conandata_patches(self)

    def configure(self):
#        self.settings.rm_safe("compiler.cppstd")
#        self.settings.rm_safe("compiler.libcxx")
        self.options["cpython/*"].env_vars = True

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        del self.info.settings.compiler

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
            destination=self.source_folder, strip_root=True)

    def generate(self):
        if self._settings_build.os != "Windows":
            tc = None
            if self.options.install_prefix:
                tc = AutotoolsToolchain(self, prefix=self.options.install_prefix)
            else:
                tc = AutotoolsToolchain(self)

            tc.generate()

    def build(self):
        apply_conandata_patches(self)
        with chdir(self, self.source_folder):
#            # README.W32
#            if self._settings_build.os == "Windows":
#                if is_msvc(self):
#                    command = "build_w32.bat --without-guile"
#                else:
#                    command = "build_w32.bat --without-guile gcc"
#                self.run(command)
#            else:
#                autotools = Autotools(self)
#                autotools.configure()
#                autotools.make()
            self.run("type python3")
            autotools = Autotools(self)
            autotools.make(target='release')
            return

    def package(self):
#        with chdir(self, self.source_folder):
#            autotools = Autotools(self)
#TODO might not work for Windows lol
#            autotools.install()

        if self.options.install_prefix:
#            save(self, os.path.join(self.package_folder, "licenses", self.name, "COPYING"), self._extract_license())
            copy(self, "COPYING",
                 src=self.source_folder,
                 dst=os.path.join(self.package_folder, str(self.options.install_prefix), "licenses", self.name)
            )
        else:
#            save(self, os.path.join(self.package_folder, "licenses", "COPYING"), self._extract_license())
            copy(self, "COPYING",
                 src=self.source_folder,
                 dst=os.path.join(self.package_folder, str(self.options.install_prefix), "licenses")
            )

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []

#        make = os.path.join(self.package_folder, "bin", "gnumake.exe" if self.settings.os == "Windows" else "make")
#        self.conf_info.define("tools.gnu:make_program", make)

        self.user_info.install_prefix = self.options.install_prefix

#        # TODO: to remove in conan v2
#        self.user_info.make = make
#        self.env_info.CONAN_MAKE_PROGRAM = make
#        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
