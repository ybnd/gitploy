import setuptools

setuptools.setup(
    name="gitploy",
    version="0.7",
    author="Yury Bondarenko",
    author_email="ybnd@tuta.io",
    url="https://github.com/ybnd/gitploy",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['PyYAML'],
)
