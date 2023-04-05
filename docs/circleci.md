# CircleCI setup

## 1. How to setup first time
- Go to https://circleci.com/ and login with your GitHub account.
- Visit `Projects` tab.
- Select your project and choose setup (if the first time setup).

## 2. Environment variable
- Read more here: https://circleci.com/docs/set-environment-variable/
- Project required variables to make the CircleCI app run without any trouble.
```shell
DJANGO_SETTINGS_MODULE=config.settings.test
COVERALLS_REPO_TOKEN={your coverall token} # use it for coverall status report, you can remove it
```
