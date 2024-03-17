import toml
import subprocess
import os

#git fetch --tags
#
#code CHANGELOG

def run(cmd:str):
    my_env = os.environ.copy()
    commandArray = cmd.split(" ")
    #print(commandArray)
    result = subprocess.run(commandArray, stdout=subprocess.PIPE, env=my_env)
    return result.stdout.decode()


# Get version tag

git_fetch = run("git fetch --tags")

version_tags = run("git tag -l *.*.*.* --sort=-version:refname").split("\n")
version_tags = [item for item in version_tags if item.strip() != ""]

# Get version from pyproject.toml
pyproject = toml.load("pyproject.toml")
pyproject_version = pyproject["tool"]["poetry"]["version"]

# load CHANGELOG
with open("CHANGELOG", "r") as file:
    changelog_data = file.read()
    changelog_has_new_version = pyproject_version in changelog_data

merge_source_branch = run("git rev-parse --abbrev-ref HEAD")
merge_source_branch = merge_source_branch.strip()
merge_target_branch = "main"

print()
print("Current branch:", merge_source_branch)
print("Merge into:", merge_target_branch)
print()
print("Version in pyproject.toml:", pyproject_version)
print("Latest version tags:", version_tags[0:5])
print("Already in CHANGELOG: ", changelog_has_new_version)
print()

if not changelog_has_new_version:
    print(f"ERROR, CHANGELOG doesn't have the version from pyproject.toml: {pyproject_version}. Check your CHANGELOG and pyproject.toml files")
    exit()

print(f"Tag latest commit with version tag {pyproject_version}... ", end="")
result = os.system(f"git tag -a {pyproject_version} -m \"Tag with {pyproject_version} on {merge_target_branch}\"")
if result != 0:
    print(f"ERROR, cannot add tag {pyproject_version}, result={result}")
    exit()

print("DONE")

print(f"Checkout target branch for merge ({merge_target_branch})...", end="")
result = os.system(f"git checkout {merge_target_branch}")
if result != 0:
    print(f"ERROR, Cannot checkout branch {merge_target_branch}, result={result}")
    exit()

print("DONE")

print(f"Merge source branch into target, {merge_source_branch} -> {merge_target_branch}...", end="")
result = os.system(f"git merge {merge_source_branch}")
if result != 0:
    print(f"ERROR, Cannot merge {merge_source_branch} into {merge_target_branch}, result={result}")
    exit()
print("DONE")


