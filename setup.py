"""Install package."""

import setuptools


setuptools.setup(
    name="OctoPrint-Toolchanger",
    version="0.0.0",
    description="Octoprint toolchanger plugin",
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
        "octoprint_toolchanger",
    ],
    entry_points={
        "octoprint.plugin": ["octoprint_toolchanger = octoprint_toolchanger"]
    },
    install_requires=[
        "OctoPrint>=1.7.3",
        "opencv-python>=4.5.5.62",
    ],
    python_requires=">=3.10",
)
