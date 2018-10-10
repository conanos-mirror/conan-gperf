
import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment


def print_environ():
    print("--- environ ---")
    for key, val in os.environ.items():
        print("\t{}:\t{}".format(key, val))
    print("--- environ ---")


class GperfConan(ConanFile):
    name = "gperf"
    version = "3.1"
    license = "GNU GPL v4"
    url = "https://github.com/conan-community/conan-gperf"
    homepage = "https://www.gnu.org/software/gperf/"
    description = "GNU gperf is a perfect hash function generator"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("cygwin_installer/2.9.0@bincrafters/stable")

    def source(self):
        url = 'http://ftp.gnu.org/pub/gnu/gperf/gperf-{version}.tar.gz'
        tools.get(url.format(version=self.version))

    def build(self):
        if self.settings.os == 'Windows':
            cygwin_bin = self.deps_env_info['cygwin_installer'].CYGWIN_BIN
            with tools.environment_append({'PATH': [cygwin_bin],
                                           'CONAN_BASH_PATH': '%s/bash.exe' % cygwin_bin}):
                with tools.vcvars(self.settings):
                    self.build_configure()
        else:
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(configure_dir="{name}-{version}".format(name=self.name, version=self.version))
            autotools.make()

    def build_configure(self):
        with tools.chdir('gperf-{version}'.format(version=self.version)):
            prefix = os.path.abspath(self.package_folder)
            win_bash = True
            prefix = tools.unix_path(prefix, tools.CYGWIN)
            args = ['--prefix=%s' % prefix]
            if self.options.shared:
                args.append('--enable-shared')
            else:
                args.append('--enable-static')
            if self.settings.build_type == 'Debug':
                args.append('--enable-debug')

            cwd = os.getcwd()
            args = ['CC="{}/build-aux/compile cl -nologo"'.format(cwd),
                    'CFLAGS="-{}"'.format(self.settings.compiler.runtime),
                    'CXX="{}/build-aux/compile cl -nologo"'.format(cwd),
                    'CXXFLAGS="-{}"'.format(self.settings.compiler.runtime),
                    'CPPFLAGS="-D_WIN32_WINNT=_WIN32_WINNT_WIN8 -I/usr/local/msvc32/include"',
                    'LDFLAGS="-L/usr/local/msvc32/lib"',
                    'LD="link"',
                    'NM="dumpbin -symbols"',
                    'STRIP=":"',
                    'AR="{}/build-aux/ar-lib lib"'.format(cwd),
                    'RANLIB=":"'
                    ]

            try:
                env_vars = dict()
                #env_vars['CC'] = 'cl'
                with tools.environment_append(env_vars):
                    env_build = AutoToolsBuildEnvironment(self, win_bash=win_bash)
                    #env_build.flags.append('-%s' % str(self.settings.compiler.runtime))
                    #env_build.flags.append('-FS')  # cannot open program database ... if multiple CL.EXE write to the same .PDB file, please use /FS
                    #print_environ()
                    #env_build.configure(args=['--help', ], build=False, host=False)
                    env_build.configure(args=args, build=False, host='i686-w64-mingw32')
                    env_build.make()
                    env_build.make(args=['install'])
            except:
                print("*"*200)
                print(open("config.log").read())


    def package(self):
        if self.settings.os != "Windows":
            with tools.chdir(self.build_folder):
                self.run("make install")

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))

