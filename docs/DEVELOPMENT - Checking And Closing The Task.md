# DEVELOPMENT - Checking And Closing The Task

## Checking workflow

Every task, when resolved, should be checked by its reporter.

We use the checking workflow only on tasks, subtasks are smaller pieces of work which do not have to be checked by the reporter (they serve for the person working on a task to organise the work into smaller chunks).

The list of tasks you need to check is [available in JIRA](#jira-filter-with-tasks-you-need-to-check).

Checking goes like this:

- when a task you reported is resolved, you can check it in two ways:
    - [locally](#checking-the-task-locally)
    - [on the reporter's Azure deployment slot](#checking-the-task-on-azure-deployment-slot)
- if the change done in the task doesn't work as it should OK, reopen the task and decribe the issue in the comment
- if the change works OK merge the pull request in the **project repo** from the corresoponding **task branch** to dev
    - this will deploy the merged code from **dev** branch to **ainergy-main-test**
- if needed (e.g, you suspect some bugs might come out of merge), after the code has been deployed from the **dev** branch, do additionall testing on **ainergy-main-test** via [solarplanner.eu](https://solarplanner.eu) (or .dk) website, by choosing "`Custom`" in the domain dropdown and entering **ainergy-main-test.azurewebsites.net** domain
- close the task in JIRA

## Checking the task locally

- pull the branch coresponding to the task
- change parameters, add or uncomment lines necesarry for testing the task in `main.py`
- run:
    ```
    python main.py
    ```
- the log output is in the `logs` folder, named after the run date and time

## Checking the task on Azure deployment slot

In order to check a task on your Azure deployment slot you need to deploy the code form the **task branch** corresponding to the task you are checking, to your deployment slot, then test it via [solarplanner.eu](https://solarplanner.eu) and custom domain corresponding to your slot.

- login to github and go to your **project repo**
    - `ainergy-main` or `ainergy-rooftop-planner`
- click "Actions" tab
- on the left there is a list of deyploments, some oF them begin with "Deploy to DEV"
- among them choose the one corresponding to your slot
    - (e.g. if Pepe was checking the task it would choose "Deploy to DEV/Pepe" which deployS to **ainergy-main-pepe** slot)
- click "Run workflow" dropdown, and choose your **task branch** from the branch dropdown (e.g. **SOLP-135-write-development-protocol**)
- click "Run workflow" button and wait for the deplyoment to finish (approx. 4 minutes)

Once the deyploment is finished, you can test the deployed code via [solarplanner.eu](https://solarplanner.eu) (or .dk) website, by choosing "`Custom`" in the domain dropdown and entering your slot's domain, eg.:

    ainergy-main-pepe.azurewebsites.net

## JIRA filter with tasks you need to check

https://aienergy.atlassian.net/issues/?filter=10106
