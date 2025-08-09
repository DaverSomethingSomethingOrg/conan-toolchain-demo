from conan import ConanFile
from conan.tools.layout import basic_layout
from conan.tools.system.package_manager import Apt, Yum

class Toolchain(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "install_prefix": [None, "ANY"],
    }
    default_options = {
        "install_prefix": None,
    }

    # For this bootstrapping phase we'll depend on OS vendor-provided compilers
    def system_requirements(self):
        Apt(self).install(["make", "cmake", "binutils", "gcc"])
        Yum(self).install(["make", "cmake", "binutils", "gcc"])

    def requirements(self):
        self.requires("binutils/2.42")

    def layout(self):
        basic_layout(self, src_folder="src")