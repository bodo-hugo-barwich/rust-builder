#!/usr/bin/python3

# @author Bodo (Hugo) Barwich
# @version 2023-08-28
# @package TextSanitizer
# @subpackage scripts/cargo_version.py

# This Module parses the Git History to find the Merge Commit for a given Commit Hash
#

import sys
import os
import os.path
import json
import yaml
from yaml import BaseLoader
from git import Repo, GitCommandError


# ==============================================================================
# Auxiliary Functions

def load_version_matrix(module_name, file_name, module_debug, module_quiet):
    matrix_result = {'success': True, 'matrix': {}}
    matrix_data = None

    try:
        stream = open(matrix_file, 'r')
        matrix_data = yaml.load(stream, Loader=BaseLoader)
        stream.close()
        matrix_result['matrix'] = matrix_data
    except Exception as e:
        if not module_quiet:
            print(
                "script '{}' - Matrix File '{}': Load File failed!".format(
                    module_name, file_name), file=sys.stderr)
            print("script '{}' - Matrix File Exception Message: {}".format(
                module_name, str(e)), file=sys.stderr)

        matrix_result['success'] = False

    if module_debug:
        print("matrix data:'{}'".format(matrix_data))

    return matrix_result


def git_fetch_tags(module_name, repository, module_debug, module_quiet):
    tags_result = {'success': True, 'tags': {}}

    try:
        for remote in repository.remotes:
            remote.fetch('--tags')

        for tag_obj in repository.tags:
            tags_result['tags'][tag_obj.name] = str(tag_obj.tag)

    except Exception as e:
        if not module_quiet:
            print("script '{}' - Tag List Exception Message: {}".format(
                module_name, str(e)), file=sys.stderr)

        tags_result['success'] = False

    if module_debug:
        print("tag list:'{}'".format(tags_result['tags']))

    return tags_result


def check_version_tags(tag_list, version_matrix):
    missing_versions = []

    for version in version_matrix['rust-versions']:
        if 'v' + version not in tag_list:
            missing_versions.append(version)

    missing_versions.sort()

    return missing_versions


# ==============================================================================
# Executing Section


# ------------------------
# Script Environment

module_file = ''
module_path = os.path.abspath(__file__)
main_dir = ''
work_dir = ''


slash_pos = module_path.rfind('/', 0)

if slash_pos != -1:
    work_dir = module_path[0: slash_pos + 1]
    module_file = module_path[slash_pos + 1: len(module_path)]
else:
    module_file = module_path

if work_dir != '':
    slash_pos = work_dir.rfind('/', 0, -1)
    if slash_pos != -1:
        main_dir = work_dir[0: slash_pos + 1]
    else:
        main_dir = work_dir


# ------------------------
# Script Parameter

matrix_command = 'first'
save_versions = []
module_output = 'plain'
module_debug = False
module_quiet = False
module_res = 0

command_list = ['print', 'check', 'save']

matrix_file = 'rust-version_matrix.yml'

if len(sys.argv) > 1:
    command = sys.argv[1]

    print("cmd: '{}'".format(command))

    if command[0: 2] != '--' and command[0] != '-':
        matrix_command = command

for arg in sys.argv:
    if arg[0: 2] == '--':
        arg = arg[2: len(arg)]
        if arg in ['plain', 'json']:
            module_output = arg
        elif arg == 'debug':
            module_debug = True
        elif arg == 'quiet':
            module_quiet = True

    elif arg[0] == '-':
        arg = arg[1: len(arg)]
        for idx in range(0, len(arg)):
            if arg[idx] == 'd':
                module_debug = True
            elif arg[idx] == 'q':
                module_quiet = True
    else:
        if arg.rfind(module_file, 0) == -1:
            if arg[0] == 'v':
                arg = arg[1: len(arg)]

            save_versions.append(arg)

if matrix_command in command_list:
    # ------------------------
    # Read the Version Matrix

    matrix_result = load_version_matrix(
        module_file,
        matrix_file,
        module_debug,
        module_quiet)

    if module_debug:
        print(
            "script '{}' - Matrix Result:\n{}".format(module_file, str(matrix_result)))

    if not matrix_result['success']:
        if not module_quiet:
            print(
                "script '{}' - Version Matrix: Read Version Matrix has failed!".format(module_file),
                file=sys.stderr)

        module_res = 1

else:
    if not module_quiet:
        print(
            "script '{}' - Matrix Command: Invalid Command '{}'!".format(module_file, matrix_command))
        print(
            "script '{}' - Matrix Command: {}".format(module_file, str(command_list)))

        module_res = 2


if matrix_command == 'print':
    # ------------------------
    # Print the Version Check Result

    if module_output == 'plain':
        if len(matrix_result['matrix']['rust-versions']) > 0:
            print("script '{}' - Rust Versions:".format(module_file))
            print("\n".join(matrix_result['matrix']['rust-versions']))
        else:
            print("script '{}' - Rust Versions: no versions registered".format(module_file))

    elif module_output == 'json':
        print("{}".format(json.dumps(matrix_result['matrix']['rust-versions'])))

    else:
        print("script '{}' - Rust Versions:\n{}".format(module_file,
                                                             str(matrix_result['matrix']['rust-versions'])))

elif matrix_command == 'check':
    # ------------------------
    # Fetch the Git Tag list

    repo = Repo('.git')
    git = repo.git

    tags_result = git_fetch_tags(module_file, repo, module_debug, module_quiet)

    if module_debug:
        print(
            "script '{}' - Tags Result:\n{}".format(module_file, str(tags_result)))

    if not tags_result['success']:
        if not module_quiet:
            print(
                "script '{}' - Git Tag list: Listing Tags has failed!".format(module_file),
                file=sys.stderr)

        module_res = 1

    # ------------------------
    # Check for missing Versions

    requested_versions = check_version_tags(
        tags_result['tags'], matrix_result['matrix'])

    if module_debug:
        print("script '{}' - Requested Versions:\n{}".format(module_file,
                                                             str(requested_versions)))

    # ------------------------
    # Print the Version Check Result

    if module_output == 'plain':
        if len(requested_versions) > 0:
            print("script '{}' - Requested Versions:".format(module_file))
            print("\n".join(requested_versions))
        else:
            print("script '{}' - Requested Versions: all versions built".format(module_file))

    elif module_output == 'json':
        print("{}".format(json.dumps(requested_versions)))

    else:
        print("script '{}' - Requested Versions:\n{}".format(module_file,
                                                             str(requested_versions)))

elif matrix_command == 'save':
    pass


if module_debug:
    print("script '{}': Script finished with [{}]".format(
        module_file, module_res))


sys.exit(module_res)
