Title: Preventing CircleCI Tasks from Running on the Same Commit
Date: 2021-09-06
Modified: 2021-09-06
Category: blog
Tags: circleci, devops
Slug: fast-pass-circleci
Authors: Charles Heckroth

A short outline on how to game CircleCI's caching mechanic to prevent sluggish builds from running on the same commit more than once.

Useful if you have some very slow CI steps and use Tags to automatically deploy from CircleCI.
In my case, our test suite could take 10 minutes to run, and had absolutely zero merit in running on the exact same codebase twice.

You could improve this to cache on a checksum of certain code contents instead of commit sha, but this is the simplest and most obvious use-case.

# [Resources](#Resources)

Below are the sources I used to figure out the exact configuration to do this.

- [On ending CircleCI jobs early](https://circleci.com/docs/2.0/configuration-reference/#ending-a-job-from-within-a-step)
- [On using environment variables in cache keys](https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables)
- [On getting the current commit as an environment variable](https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables)

# [Saving Successful Status](#Saving Successful Status)

## [Raw code](#Raw code)

```yaml
version: 2.1
jobs:
  build:
    docker:
      - image: circleci/python:3.7.3
    steps:
      - restore_cache:
          key: "{{ .Environment.CIRCLE_SHA1 }}"
      - run:
          name: Check for previous success on same commit
          command: |
            if test -f ".success"; then
              echo "Previous successful build exists. Pre-passing tests..."
              circleci-agent step halt
            else
              echo "Commit has no successful cached build, running tests..."
            fi
      - run:
          command: execute-my-test
      - run:
          command: "touch .success"
      - save_cache:
          key: "{{ .Environment.CIRCLE_SHA1 }}"
          paths:
            - ".success"

workflows:
  main:
    jobs:
      - build
```


## [Breakdown](#Breakdown)

**1) restore_cache**

This checks for a cache with the current commit as its key. We set this as the last step of the job.

**2) run success check**

This is where we use the circleci-agent linked in [Resources](#Resources).

We simply check for a file's presence and end the build with circleci-agent if it exists.

This file is created and cached at the end of the job.

**3) run execute-my-test**

This is a placeholder for whatever your actual job is supposed to do. In my case its a very large and sluggish django test suite.

**4) run touch .success**

Simply create an empty file. I named it .success, but if you already have a file with that name in your project, you want to name it something different. Make sure whatever you name it is reflected in **2) run success check** as well.

**5) save_cache**

Put the file you just created in a cache keyed by the current commit hash.

This will be restored in (1) and caught in (2) to end the bulid early if a build is run on this same commit again.

This step will only be run if every step before it was successful, so it is safe at this point to store the successful state. Make sure its the last step!


## Notes

1. There might be a smarter way to do this. If so, please let me know!
2. Since this is using a cache, it is a short-term solution. I don't know how long CircleCI keeps its build caches around, but if you need to skip jobs based on previous success months or years in later, you'll have to think of something else.
3. This still runs the job. There are workflow filters that can completely skip the job, but no way to base that on past success that I know of.
