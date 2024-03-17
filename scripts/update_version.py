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

new_version_tag = version_tags[0].split(".")
new_version_tag[3] = str(int(new_version_tag[3]) + 1)
new_version_tag = ".".join(new_version_tag)

# Get version from pyproject.toml
pyproject = toml.load("pyproject.toml")
pyproject_version = pyproject["tool"]["poetry"]["version"]

# load CHANGELOG
with open("CHANGELOG", "r") as file:
    changelog_data = file.read()
    changelog_has_new_version = new_version_tag in changelog_data


print()
print("Version in pyproject.toml:", pyproject_version)
print("Latest version tags:", version_tags[0:5])
print("New version tag: ", new_version_tag)
print("Already in CHANGELOG: ", changelog_has_new_version)
print()

# Update pyproject.toml


if (pyproject["tool"]["poetry"]["version"] != new_version_tag):
    pyproject["tool"]["poetry"]["version"] = new_version_tag
    print(f"Writing {new_version_tag} version to pyproject.toml... ", end="")
    with open("pyproject.toml", "w", newline='\n') as file:
        toml.dump(pyproject, file)
    print("DONE")

# Update CHANGELOG

changelog_line = 3

if not changelog_has_new_version:
    changelog_line = 3
    print(f"Writing {new_version_tag} version to CHANGELOG... ", end="")
    with open("CHANGELOG", "w", newline='\n') as file:
        file.write(f"{new_version_tag}\n\n\n\n" + changelog_data)
    print("DONE")

print("Open CHANGELOG... ", end="")
os.system(f"code --goto CHANGELOG:{changelog_line}")
print("DONE")

