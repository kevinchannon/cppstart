from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


class proj_nameRecipe(ConanFile):
    name = "proj_name"
    version = "0.0.1"

    # Optional metadata
    license = "$license_name"
    author = "$copyright_name $author_email"
    url = "$url"
    description = "Here is a long description of the awesome proj_name project and what it can do for its users."
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["proj_name"]