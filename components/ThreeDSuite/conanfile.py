from conan import ConanFile
from conan.tools.layout import basic_layout

class ThreeDSuite(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "install_prefix": [None, "ANY"],
    }
    default_options = {
        "install_prefix": None,
    }

    def requirements(self):
        self.requires("openusd/")
        self.requires("moonray/")
        self.requires("godot/")
        self.requires("renderman/")
        self.requires("blender/")

    def layout(self):
        basic_layout(self, src_folder="src")
