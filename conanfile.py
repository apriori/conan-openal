from conans import CMake, ConanFile, tools
import os

class OpenALConan(ConanFile):
    name = "openal"
    version = "1.18.2"
    md5 = "fa2cb3df766ab5976c86efbcc1d24d68"
    description = "OpenAL Soft is a software implementation of the OpenAL 3D audio API."
    url = "http://github.com/bincrafters/conan-openal"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "source_subfolder"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    def configure(self):
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("libalsa/1.1.5@conan/stable")

    def source(self):
        source_url = "https://github.com/kcat/openal-soft"
        tools.get("{0}/archive/openal-soft-{1}.tar.gz".format(source_url, self.version), self.md5)
        extracted_dir = "openal-soft-openal-soft-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        
    def build(self):
        cmake = CMake(self)
        if self.settings.compiler != 'Visual Studio':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        pass
        
    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["OpenAL32"]
        else:
            self.cpp_info.libs = ["openal"]
        self.cpp_info.includedirs = ["include", "include/AL"]
