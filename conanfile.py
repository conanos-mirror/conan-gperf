import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment


class GperfConan(ConanFile):
    name = "gperf"
    version = "3.1"
    license = "GNU GPL v4"
    url = "https://github.com/conan-community/conan-gperf"
    homepage = "https://www.gnu.org/software/gperf/"
    description = "GNU gperf is a perfect hash function generator"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    @property
    def is_msvc(self):
        return self.settings.compiler == 'Visual Studio'

    @property
    def is_mingw_windows(self):
        return self.settings.os == 'Windows' and self.settings.compiler == 'gcc' and os.name == 'nt'

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("cygwin_installer/2.9.0@bincrafters/stable")

    def source(self):
        url = 'http://ftp.gnu.org/pub/gnu/gperf/gperf-{version}.tar.gz'
        tools.get(url.format(version=self.version))

    def build(self):
        if self.is_msvc:
            with tools.vcvars(self.settings):
                self.build_configure()
        else:
            self.build_configure()

    def build_configure(self):
        with tools.chdir('gperf-{version}'.format(version=self.version)):
            args = []
            if self.options.shared:
                args.extend(['--enable-shared', '--disable-static'])
            else:
                args.extend(['--enable-static', '--disable-shared'])
            if self.settings.build_type == 'Debug':
                args.append('--enable-debug')

            cwd = os.getcwd()

            win_bash = self.is_msvc or self.is_mingw_windows
            if self.is_msvc:
                args.extend(['CC={}/build-aux/compile cl -nologo'.format(cwd),
                             'CFLAGS=-{}'.format(self.settings.compiler.runtime),
                             'CXX={}/build-aux/compile cl -nologo'.format(cwd),
                             'CXXFLAGS=-{}'.format(self.settings.compiler.runtime),
                             'CPPFLAGS=-D_WIN32_WINNT=_WIN32_WINNT_WIN8 -I/usr/local/msvc32/include',
                             'LDFLAGS=-L/usr/local/msvc32/lib',
                             'LD=link',
                             'NM=dumpbin -symbols',
                             'STRIP=:',
                             'AR={}/build-aux/ar-lib lib'.format(cwd),
                             'RANLIB=:'])

            env_build = AutoToolsBuildEnvironment(self, win_bash=win_bash)
            env_build.configure(args=args)
            env_build.make()
            env_build.install()

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
