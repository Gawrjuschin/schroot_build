import argparse
import json
from pathlib import Path

SYSTEMS = {
    "debian-trixie": {
        "display": "Debian 13 Trixie",
        "gcc": "14",
        "root": "/srv/chroot/debian-trixie",
        "packs": [
            "DEB",
            "TGZ",
        ],
    },
    "debian-forky": {
        "display": "Debian 14 Forky",
        "gcc": "16",
        "root": "/srv/chroot/debian-forky",
        "packs": [
            "DEB",
            "TGZ",
        ],
    },
    "ubuntu-noble": {
        "display": "Ubuntu 24 Noble",
        "gcc": "14",
        "root": "/srv/chroot/ubuntu-noble",
        "packs": [
            "DEB",
            "TGZ",
        ],
    },
    "ubuntu-plucky": {
        "display": "Ubuntu 26 Plucky",
        "gcc": "15",
        "root": "/srv/chroot/ubuntu-plucky",
        "packs": [
            "DEB",
            "TGZ",
        ],
    },
}


ARCHES = frozenset(
    {
        "i686",
        "x86_64",
        "aarch64",
    }
)

BUILD_TYPES = frozenset(
    {
        "Debug",
        "Release",
    }
)


def generate_presets(systems: list[str], architectures: list[str]) -> dict:
    configure_presets = [
        {
            "name": "schroot-base",
            "hidden": True,
            "generator": "Ninja Multi-Config",
            "binaryDir": "${sourceDir}/build/${presetName}",
            "toolchainFile": "${sourceDir}/cmake/toolchains/schroot-toolchain.cmake",
            "cacheVariables": {"CMAKE_EXPORT_COMPILE_COMMANDS": "ON"},
        },
        *[
            {
                "name": f"arch-{ arch }",
                "hidden": True,
                "cacheVariables": {"SCHROOT_TARGET_PROCESSOR": arch},
            }
            for arch in architectures
        ],
        *[
            {
                "name": system,
                "hidden": True,
                "cacheVariables": {
                    "SCHROOT_GCC_VERSION": SYSTEMS[system]["gcc"],
                    "SCHROOT_ROOT": SYSTEMS[system]["root"],
                },
            }
            for system in systems
        ],
        *[
            {
                "name": f"{ system }-{ arch }-config",
                "displayName": f'Configure { SYSTEMS[system]["display"]} { arch }',
                "inherits": ["schroot-base", f"arch-{ arch }", system],
            }
            for system in systems
            for arch in architectures
        ],
    ]

    build_presets = [
        {
            "name": f"{ system }-{ arch }-build-{ build_type.lower() }",
            "configurePreset": f"{ system }-{ arch }-config",
            "configuration": build_type,
        }
        for system in systems
        for arch in architectures
        for build_type in BUILD_TYPES
    ]

    package_presets = [
        {
            "name": f"{ system }-{ arch }-pack",
            "displayName": f'Package { SYSTEMS[system]["display"] } { arch }',
            "description": f'Generate packages for { SYSTEMS[system]["display"] } { arch } using CPack',
            "configurePreset": f"{ system }-{ arch }-config",
            "generators": SYSTEMS[system]["packs"],
            "configurations": ["Release"],
        }
        for system in systems
        for arch in architectures
    ]

    workflow_presets = [
        {
            "name": f"{ system }-{ arch }-full",
            "displayName": f'Configure, Build and Pack ({ SYSTEMS[system]["display"] } { arch })',
            "description": f'Configure, build Release, and generate packages ({ SYSTEMS[system]["display"] } { arch }) in one command',
            "steps": [
                {
                    "type": "configure",
                    "name": f"{ system }-{ arch }-config",
                },
                {
                    "type": "build",
                    "name": f"{ system }-{ arch }-build-release",
                },
                {
                    "type": "package",
                    "name": f"{ system }-{ arch }-pack",
                },
            ],
        }
        for system in systems
        for arch in architectures
    ]

    return {
        "version": 6,
        "configurePresets": configure_presets,
        "buildPresets": build_presets,
        "packagePresets": package_presets,
        "workflowPresets": workflow_presets,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--systems", nargs="+", required=True, choices=SYSTEMS.keys())
    parser.add_argument("--architectures", nargs="+", required=True, choices=ARCHES)
    parser.add_argument("--output", default="CMakeUserPresets.generated.json")
    args = parser.parse_args()

    with open(args.output, "w+", encoding="utf-8") as f:
        json.dump(
            generate_presets(args.systems, args.architectures),
            f,
            indent=2,
            ensure_ascii=False,
        )


if __name__ == "__main__":
    main()
