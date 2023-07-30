# Development - Working on a task

## 1. Starting the task

- in your JIRA task create a new branch from the **dev** branch (we’ll call the new branch “**task branch**”) in your project repo:  
    - either `ainergy-main` or `ainergy-rooftop-planner` (we’ll call it “**project repo**”)
    - example task branch: **SOLP-135-write-development-protocol**
- pull the new task branch of **project repo** to your local machine
- if task requires work on `aiecommon` package, then in the same JIRA task create a branch also in `aiecommon` repo from **main** branch
    - pull the new task branch of `aiecommon` to your local machine
- run poetry install:
    ```
    poetry install
    ```

## 2. Working on the task

### 2.1. General

- in all repos always work on your task branches
- changes which are related to the algorithm and don't affect the API part implemented in Azure you can test them during development by running `python main.py`
- changes which are related to of somehow affect the API part implemented in Azure should be tested during th development by locally running the Azure functions server or by 
[deploying the code to the developer slot](#deploying-the-code-to-the-developer-slot)
- **if you have changes which are not commited or pushed in `aiecommon` repo, DO NOT RUN `poetry install` in your project repo!!!**
    - it will reinstall the `aiecommon` package to the version stated in the `pyproject.toml` of your **project repo** and delete your changes in `aiecommon` repo


### 2.2. Deploying the code to the developer slot

Each developer has its own deplyoment slot, where it can test directly on Azure the code in its branch. Deployment is done using Github actions:

- login to github and go to your **project repo**
- click "Actions" tab
- on the left there is a list of deyploments, some od them begin with "Deploy to DEV"
- among them choose the one corresponding to your slot
- click "Run workflow" dropdown, and choose your **task branch** from the branch dropdown (e.g. **SOLP-135-write-development-protocol**)
- click "Run workflow" button and wait for the deplyoment to finish (approx. 4 minutes)

Once the deyploment is finished, you can test the deployed code via [solarplanner.eu](https://solarplanner.eu) (or .dk) website, by choosing "`Custom`" in the domain dropdown and entering your slot's domain, eg.:

    ainergy-main-pepe.azurewebsites.net

## 3. Finishing the task - a) changes only in **project repo**

- run poetry export:
    ```
    scripts/poetry-export.cmd
    ```
- if the script generated some changes, commit it to your **task branch** and push it
- create a pull request form your **task branch** to **dev**
- go to the task in JIRA and mark it as resolved

## 4. Finishing the task - b) with changes in `aiecommon`

In this case you need to finish the task in two steps, one in the `aiecommon` repo, the other in the **project repo**.

### 4.1. In the `aiecommon` repo:

- run update_version script:
    ```
    scripts/update_version.cmd
    # Use backslash on Windows: scripts\update_version.cmd
    ```
    _the script will update `pyproject.toml` and `CHANGELOG` with new version and open `CHANGELOG` in vscode [^1]_ 
- in the opened `CHANGELOG` describe the changes under the new version, e.g.:
    ```
    0.1.9.9
    
    write development protocol in the docs
    
    0.1.9.8

    Rename paths to match new data folder structures
    ...
    ```
- commit the changes to your task branch
- run tag_version script:
    ```
    scripts/tag_version.cmd
    # Use backslash on Windows: scripts\tag_version.cmd
    ```
    _the script will tag the current commit with new version tag and merge current branch into main_ 

- push your **main** branch

### 4.2. In the **project repo**:

- change rev for aiecommon in `pyproyect.toml` to the new version (e.g. 0.1.9.9):
    ```python
    aiecommon = {git = "https://github.com/AI-nergy/aiecommon.git", rev = "0.1.9.9", develop = true}
    ```
- do all the steps listed in ["3. Finishing the task - a) changes only in **project repo**](#3-finishing-the-task---a-changes-only-in-project-repo)"


## Footnotes

[^1] the update_version script automates several tasks:

- fetch the latest version tags from remote and generate a new version tag
- update pyproject.toml with the new version tag
- add new version tag to CHANGELOG and open it in vscode



[//]: <> ()
[//]: <> ()
[//]: <> (
    - check if there's a newer version of the package in the remote repo
        - this is done on your local machine by doing fetch, then checking the newest version tag
        - or by going to the `aiecommon` repo on github.com and checking the list of tags there 
    - if there's a newer version of the package, then merge **main** into your task branch to pick up that version changes
    - increase the version of the package, in `pyproject.toml`, e.g.:
        ```toml
        [tool.poetry]
        name = "aiecommon"
        version = "0.1.9.7"        ```
)