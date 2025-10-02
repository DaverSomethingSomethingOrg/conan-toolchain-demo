from conan import ConanFile
from conan.tools.layout import basic_layout
from conan.tools.system.package_manager import Apt, Yum

class Toolchain(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    author = "David L. Armstrong"

    options = {
        "install_prefix": [None, "ANY"],
    }
    default_options = {
        "install_prefix": None,
        "cpython/*:with_tkinter": False, # Don't want to trigger X11 system package installs
    }

    def system_requirements(self):
        Apt(self).install(["opt+toolchain-make",
                           "opt+toolchain-cmake",
                           "opt+toolchain-gcc",
                           "opt+toolchain-binutils",
                          ])
        Yum(self).install(["opt-toolchain-make",
                           "opt-toolchain-cmake",
                           "opt-toolchain-gcc",
                           "opt-toolchain-binutils",
                          ])

    def requirements(self):
        self.requires("cmake/4.1.0")
        self.requires("make/4.4.1")
        self.requires("m4/1.4.20", override=True) # autoconf version conflict
        self.requires("flex/2.6.4")
        self.requires("bison/3.8.2")
        self.requires("binutils/2.42")
        self.requires("gcc/12.2.0")

        self.requires("fmt/11.2.0", override=True) # ccache version conflict
        self.requires("xxhash/0.8.3", override=True) # rsync version conflict

        self.requires("autoconf/2.72", override=True) # automake version conflict
        self.requires("automake/1.16.5")

        self.requires("gtest/1.16.0")
        self.requires("cppunit/1.15.1")
#        self.requires("elfutils/0.190", override=True)
        self.requires("expat/2.7.1")
        self.requires("freetype/2.13.3")
        self.requires("gdbm/1.23")
        self.requires("gettext/0.22.5")
#        self.requires("glib/2.81.0")
#        self.requires("gstreamer/1.24.7")

#        self.requires("ffmpeg/6.1.1")
#        self.requires("openjpeg/2.5.2")
#        self.requires("openh264/2.4.1")
#        self.requires("pkgconf/2.2.0", override=True)

        self.requires("llvm-core/19.1.7")

        self.requires("meson/1.7.2")
        self.requires("ninja/1.12.1")
        self.requires("bazel/7.2.1")

        self.requires("doxygen/1.14.0")

        self.requires("openjdk/21.0.2")

        self.requires("cpython/3.12.7")

        # doxygen and cpython have a version conflict on util-linux-libuuid
        self.requires("util-linux-libuuid/2.39.2", override=True)

        self.requires("nodejs/20.16.0")

        self.requires("rusty-cpp/0.1.12")

#        self.requires("7zip/23.01") # "Invalid: Only Windows supported"
#        self.requires("gtk/4.6.2") #broken?

        self.requires("boost/1.88.0")
        self.requires("openssh/9.9p1")

        self.requires("bzip2/1.0.8")
        self.requires("ccache/4.11")

#        self.requires("imagemagick/7.0.11-14")
        self.requires("libmemcached/1.0.18")
        self.requires("libiconv/1.18", override=True)

        self.requires("openmpi/4.1.6")
#        self.requires("protobuf/6.30.1")
#        self.requires("rsync/3.2.7")
#        self.requires("ruby/3.1.0")
        self.requires("scons/4.6.0")
        self.requires("tar/1.35")
        self.requires("zstd/1.5.6", override=True)



    def layout(self):
        basic_layout(self, src_folder="src")
