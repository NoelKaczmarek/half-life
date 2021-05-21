from setuptools import setup

setup(
    name='half-life-sim',
    version='1.0',
    author='Noel Kaczmarek',
    author_email="noel@kaczmarek.eu",
    packages=['half_life'],
    setup_requires=['setuptools'],
    install_requires=['desktop-app'],
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['*.svg', '*.ico', 'desktop-app.json']},
    entry_points={
        'console_scripts': ['half-life = desktop_app:entry_point'],
        'gui_scripts': ['half-life-gui = desktop_app:entry_point'],
    },
)