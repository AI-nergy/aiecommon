# Development - Working wiht aiecommon


## 1) In aiecommon repo

1. Commit and push your changes to `main` branch

2. Update version

```bash
cd .venv/src/aiecommon/
sh scripts/update_version.sh
```

It will update the version in `pyproject.toml` file for `aiecommon` and open the `CHANGELOG` file.

3. Write the changes in `CHANGELOG` and save it

4. Commit your changes to `main` branch and push them

5. Tag the branch with the version tag:
```bash
sh scripts/tag_branch_wtih_version.sh
```

5. Push your changes to `main` branch, ensure to push the tags:
```bash
git push --tags
```


## 2) In your base repo (rooftop, optimizer)

1. Change aiecommon version in `pyproject.toml`

Example:

```toml
aiecommon = {git = "https://github.com/AI-nergy/aiecommon.git", rev = "v0.2.0.26", develop = true}
```

2. Update aiecommon:

```bash
poetry update aiecommon
```

3. Commit and push your changes to your task branch