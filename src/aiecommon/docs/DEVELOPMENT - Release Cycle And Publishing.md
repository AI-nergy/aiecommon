# DEVELOPMENT - Release Cycle And Publishing

# Release Cycle

TODO

# Publishing A Release

TODO: elaborate the steps

- forbid the commits to dev branch
- check the last deployment from dev branch was successfull - github Actions
- test on test slot
- create a pull request from dev to main
- merge teh pull request
    - automatically deployed to stage slot in 4 min
- when deployed do a quick test on the stage slot
- allow the commits to dev branch
- test thoroughly on stage via solarplanner.eu (few people, several days)
- when tested and all OK, do a switch stage -> prod in Azure Portal
- quick test
- if there's a fatal error, switch back prod -> stage
- test in production
