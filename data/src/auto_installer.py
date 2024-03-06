import os

Requires = [
    'pygame',
    '-i https://test.pypi.org/simple/ JPyDB',
    'xlwt'
]

class AutoInstaller:
    def __init__(self):
        pass

    def Install(self, item):
        try:
            print(f"[AutoInstaller] {item}")
            os.system(f"pip install {item}")
        except Exception as e:
            print(e)

    def InstallAll(self):
        for item in Requires:
            self.Install(item)