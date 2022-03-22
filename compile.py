#!/usr/bin/python


import os
import re
import json
import stat
import shutil
import hashlib
import subprocess
import platform
import argparse
from pathlib import Path

SYSTEMS = ["Linux", "MacOS", "Windows"]

SCRIPT = os.path.abspath(os.path.dirname(__file__))

ROOT = SCRIPT

DEPENDENCIES = {
    "inkscape": "/usr/bin/inkscape",
}

ROOT_GRANTURISMOTRACKER = os.path.join(ROOT, "granturismotracker")

RESOURCE_PATHS = [
    os.path.join(ROOT_GRANTURISMOTRACKER, "static/images")
]

RESOURCE_EXTENSIONS = [
    "png"
]

RESOURCE_MAPPINGS = [
    ["svg", "png"]
]


def run():
    system = None
    if platform.system() == "Linux":
        system = "Linux"
    if platform.system() == "Darwin":
        system = "MacOS"
    if platform.system() == "Windows":
        system = "Windows"
    if not system in SYSTEMS:
        print("[Warning] Running this script is not supported on your system. You are running on {0}, the supported systems are {1}.".format(system, SYSTEMS))
        return
    parser = argparse.ArgumentParser(description="GranTurismoTracker compilation script.")
    parser.add_argument("what", metavar="what", type=str, nargs=1, default="None", choices=["resources"], help="What to compile? [resources]")
    dependencies = {}
    for dependency in DEPENDENCIES:
        default = DEPENDENCIES[dependency] if Path(DEPENDENCIES[dependency]).is_file() else None
        parser.add_argument("--{0}".format(dependency), metavar=dependency, type=str, nargs=1, default=default, help="The path to the {0} dependency.".format(dependency))
    args = parser.parse_args()
    for dependency in DEPENDENCIES:
        executable = args.__dict__[dependency]
        dependencies[dependency] = None
        try:
            dependencies[dependency] = executable if Path(executable).is_file() else None
        except:
            dependencies[dependency] = None
    if args.what != None:
        globals()["compile_{0}".format(args.what[0])](system, dependencies)


def compile_resources(_system, _dependencies):
    if _system != "Linux":
        print("[Error] Compiling the resources is not supported yet for {0}.".format(_system))
        return
    if not check_dependencies(_dependencies, ["inkscape"]):
        return
    for resource_path in RESOURCE_PATHS:
        for resource_extension in RESOURCE_EXTENSIONS:
            for path in Path(resource_path).rglob("*.{0}.import".format(resource_extension)):
                if not file_exists("{0}".format(str(path)).replace(".import", "")):
                    remove_file(str(path))
        for resource_mapping in RESOURCE_MAPPINGS:
            if len(resource_mapping) != 2:
                continue
            resource_extension_source = resource_mapping[0]
            resource_extension_target = resource_mapping[1]
            resource_files_source = []
            resource_files_source_hash = []
            resource_files_source_import = []
            resource_files_target = []
            resource_files_target_import = []
            for path in Path(resource_path).rglob("*.{0}".format(resource_extension_source)):
                resource_files_source.append(str(path))
            for path in Path(resource_path).rglob("*.{0}.hash".format(resource_extension_source)):
                resource_files_source_hash.append(str(path))
            for path in Path(resource_path).rglob("*.{0}.import".format(resource_extension_source)):
                resource_files_source_import.append(str(path))
            for path in Path(resource_path).rglob("*.{0}".format(resource_extension_target)):
                resource_files_target.append(str(path))
            for path in Path(resource_path).rglob("*.{0}.import".format(resource_extension_target)):
                resource_files_target_import.append(str(path))
            for resource_file_source_hash in resource_files_source_hash:
                resource_file_source = resource_file_source_hash.replace(".{0}.hash".format(resource_extension_source), ".{0}".format(resource_extension_source))
                if not file_exists(resource_file_source):
                    if file_exists(resource_file_source_hash):
                        remove_file(resource_file_source_hash)
            for resource_file_source_import in resource_files_source_import:
                resource_file_source = resource_file_source_import.replace(".{0}.import".format(resource_extension_source), ".{0}".format(resource_extension_source))
                if not file_exists(resource_file_source):
                    if file_exists(resource_file_source_import):
                        remove_file(resource_file_source_import)
            for resource_file_target_import in resource_files_target_import:
                resource_file_target = resource_file_target_import.replace(".{0}.import".format(resource_extension_target), ".{0}".format(resource_extension_target))
                if not file_exists(resource_file_target):
                    if file_exists(resource_file_target_import):
                        remove_file(resource_file_target_import)
            for resource_file_target in resource_files_target:
                resource_file_target_import = resource_file_target + ".import"
                resource_file_source = resource_file_target.replace(".{0}".format(resource_extension_target), ".{0}".format(resource_extension_source))
                if not file_exists(resource_file_source):
                    if file_exists(resource_file_target):
                        remove_file(resource_file_target)
                    if file_exists(resource_file_target_import):
                        remove_file(resource_file_target_import)
            for resource_file_source in resource_files_source:
                resource_file_source_hash = resource_file_source + ".hash"
                resource_file_target = resource_file_source.replace(".{0}".format(resource_extension_source), ".{0}".format(resource_extension_target))
                hash_old = get_file_hash_old(resource_file_source)
                hash_new = get_file_hash_new(resource_file_source)
                if not hash_old or hash_old != hash_new or not file_exists(resource_file_target):
                    with open(os.path.devnull, "w") as f:
                        create_tree(resource_file_target)
                        subprocess.run("{0} {1} --vacuum-defs -o {1}".format(_dependencies["inkscape"], resource_file_source, resource_file_source).split(), stdout=f, stderr=f)
                        subprocess.run("{0} {1} -o {2}".format(_dependencies["inkscape"], resource_file_source, resource_file_target).split(), stdout=f, stderr=f)
                    hash_new = get_file_hash_new(resource_file_source)
                    with open(resource_file_source_hash, "w+") as f:
                        f.write(hash_new)


def check_dependencies(_available, _required):
    unavailable = []
    for dependency in _required:
        if not dependency in _available or _available[dependency] == None:
            unavailable.append(dependency)
    if len(unavailable) > 0:
        print("[Warning] Some dependencies ({0}) are unavailable, check the help (-h) to see how to define them.".format(unavailable))
        return False
    return True


def get_file_hash_old(_file):
    if not file_exists(_file + ".hash"):
        return None
    hash_sha256 = None
    with open(_file + ".hash", "r") as f:
        hash_sha256 = f.read()
    return hash_sha256


def get_file_hash_new(_file):
    if not file_exists(_file):
        return None
    hash_sha256 = hashlib.sha256()
    with open(_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def file_exists(_path):
    if not os.path.exists(_path):
        return False
    if not os.path.isfile(_path):
        return False
    return True


def tree_exists(_path):
    if not os.path.exists(_path):
        return False
    if not os.path.isdir(_path):
        return False
    return True


def copy_file(_path_source, _path_target):
    shutil.copyfile(_path_source, _path_target)


def copy_tree(_path_source, _path_target):
    shutil.copytree(_path_source, _path_target)


def move_file(_path_source, _path_target):
    if not str(os.path.realpath(_path_source)).startswith(ROOT):
        return
    if not str(os.path.realpath(_path_target)).startswith(ROOT):
        return
    shutil.move(_path_source, _path_target)


def remove_file(_path):
    if not str(os.path.realpath(_path)).startswith(ROOT):
        return
    if os.path.exists(_path):
        os.remove(_path)


def create_tree(_path):
    if not str(os.path.realpath(_path)).startswith(ROOT):
        return
    os.makedirs(os.path.dirname(_path), exist_ok=True)


def remove_tree(_path):
    if not str(os.path.realpath(_path)).startswith(ROOT):
        return
    shutil.rmtree(_path, ignore_errors=True)


run()
