
#from conan.packager import ConanMultiPackager
#
#
#if __name__ == "__main__":
#    builder = ConanMultiPackager()
#    builder.add_common_builds(shared_option_name="gperf:shared", pure_c=True)
#    builder.run()

from bincrafters import build_template_default

if __name__ == "__main__":

    builder = build_template_default.get_builder(pure_c=True)

    builder.run()