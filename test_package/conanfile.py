from conans import ConanFile


class GperfTestConan(ConanFile):
    def test(self):
        self.run('gperf --version', run_environment=True)
