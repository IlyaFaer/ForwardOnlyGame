from setuptools import setup

setup(
    name="Forward Only",
    version="0.9.1",
    author="IlyaFaer",
    author_email="ilya.faer.gurov@gmail.com",
    description="Forward Only - Seepage, the game",
    license="https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md",
    url="https://github.com/IlyaFaer/ForwardOnlyGame",
    options={
        "build_apps": {
            "platforms": [
                "win_amd64",
                "win32",
                "macosx_10_6_x86_64",
                "manylinux1_x86_64",
            ],
            "include_patterns": [
                "**/*.bam",
                "**/*.ico",
                "**/*.jpg",
                "**/*.jpeg",
                "**/*.mp3",
                "**/*.ogg",
                "**/*.png",
                "**/*.ptf",
                "**/*.ttf",
            ],
            "include_modules": {"*": ["__builtin__", "shelve", "dbm"]},
            "gui_apps": {"Forward Only": "main.py"},
            "plugins": ["pandagl", "p3fmod_audio", "p3openal_audio"],
        }
    },
)
