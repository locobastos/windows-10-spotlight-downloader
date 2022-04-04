import sys
import setuptools


if sys.version_info < (3, 10):
    sys.exit('Python>=3.10 is required.')

setuptools.setup(
    name="windows-10-spotlight-downloader",
    version="1.0.1",
    url="https://github.com/locobastos/windows-10-spotlight-downloader",

    description="Download 1920x1080p images from Windows 10 Spotlight site",
    license='MIT License',

    packages=setuptools.find_packages(),
    platforms='any',

    install_requires=[
        'fake-useragent-ex >= 0.1.12',
        'beautifulsoup4'
    ]
)
