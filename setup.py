"""Install package."""

import os
import setuptools
import packaging.version


def get_version_num() -> str:
    input_ver = os.environ.get("TOOLCHANGER_PLUGIN_RELEASE_VERSION", "0.0.0dev0")
    return str(packaging.version.parse(input_ver))


setuptools.setup(
    name="OctoPrint-Toolchanger",
    version=get_version_num(),
    description="E3D Toolchanger plugin",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[],
    license="MIT",
    author="Ilja Orlovs",
    author_email="vrghost@gmail.com",
    url="https://github.com/VRGhost/OctoPrint-Toolchanger",
    package_dir={"": "src"},
    zip_safe=False,
    include_package_data=True,
    packages=setuptools.find_packages(where="src"),
    py_modules=[
        "octoprint_toolchanger", "octoprint_virtual_toolchanger"
    ],
    entry_points={
        "octoprint.plugin": [
            "octoprint_toolchanger = octoprint_toolchanger",
            "octoprint_virtual_toolchanger = octoprint_virtual_toolchanger",
        ]
    },
    install_requires=[
        "OctoPrint>=1.8.6",
        # "opencv-python>=4.5.5.62",
    ],
    python_requires=">=3.10",
)
