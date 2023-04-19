Title: Upgrading a Cloudformation-managed RDS Instance Engine
Date: 2023-04-19
Modified: 2023-04-19
Category: blog
Tags: aws, rds, infrastructure, devlog
Slug: cloudformation-rds-engine-upgrade
Authors: Charles Heckroth

I manage all of my AWS infrastructure with Cloudformation, and have for several years. While this is usually very helpful, sometimes there are snags with one of the many AWS services and how cloudformation attempts to interact with them.

Upgrading my database version was one of these. This post outlines how I upgraded my in-use postgres database from 11 to 15 with a mix of manual operations and cloudformation changeset deployments.


# The Details

I have an RDS instance and its parameter group managed by Cloudformation (among other things, but the use-case here is simplified).

This instance has been in operation for a number of years, and is using Postgres11, which is on its way out the door this year. I want to upgrade my database, but I don't want a significant desync with cloudformation. I want to ensure that I can upgrade my database and continue to manage with cloudformation safely.

# The Problem

Below is a sample from my configuration. Most properties have been omitted, because the real configuration is very long. So I have left just the bare minimum.

```yaml
  DBParameters:
    Type: AWS::RDS::DBParameterGroup
    Properties:
      Description: "DB setetings"
      Family: "postgres11"
      Parameters:
        log_statement: ddl
        log_min_duration_statement: 500

  DB:
    Type: AWS::RDS::DBInstance
    Properties:
      DBParameterGroupName: !Ref DBParameters
      EnableCloudwatchLogsExports:
        - "postgresql"
        - "upgrade"
      EnablePerformanceInsights: True
      Engine: "postgres"
      MultiAZ: False
      Port: 5432
      PubliclyAccessible: False
      StorageType: "gp2"
```

My first attempt to fix this is to simply change `DBParameters::Properties::Family` to `postgres14` and execute the cloudformation changeset. This simply doesn't work. I don't really know why, but I could not find a way to actually enact this change via cloudformation (Maybe if you specify the minor version in `DB::Properties::EngineVersion`, but I don't really want to do that.)

# The Solution

## Manual Execution

Ultimately, I just upgraded the database manually.

1. Open the database in the RDS console
2. Click "Modify" in the top-right corner
3. Change the DB Engine Version to the latest of whatever family you want.
4. "Additional Configuration" section should also be upgraded to the correct family
5. Execute the upgrade

This could take around 30 minutes to finish. It will incur downtime when the database actually restarts.
In a future post, I will outline my approach to tracking downtime from major infrastructure changes to appropriately plan scheduled maintenance in production environments.

## Catching Up with CloudFormation

WARNING: This step ALSO will incur downtime. To sync up, the DBParameterGroup must be recreated, which requires a database restart. When upgrading manually, the parameter group is set set to "default".

Below is the updated config. All that has changed is `DBParameters::Properties::Family` from `postgres11` to `postgres14`.

Simply execute the changeset as you would any other changeset.

In my case, I execute

```
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name my-stack-develop \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides Env=develop \
  --no-execute-changeset
```

and then confirm the changeset & manually execute in the Cloudformation console.


```yaml
  DBParameters:
    Type: AWS::RDS::DBParameterGroup
    Properties:
      Description: "DB setetings"
      Family: "postgres14"
      Parameters:
        log_statement: ddl
        log_min_duration_statement: 500

  DB:
    Type: AWS::RDS::DBInstance
    Properties:
      DBParameterGroupName: !Ref DBParameters
      EnableCloudwatchLogsExports:
        - "postgresql"
        - "upgrade"
      EnablePerformanceInsights: True
      Engine: "postgres"
      MultiAZ: False
      Port: 5432
      PubliclyAccessible: False
      StorageType: "gp2"
```

## Future Effects

As far as I can tell, once the manual execution & cloudformation follow-up have been completed, there are no more issues. Ultimately, it is the same state that you would expect to be in if the original idea of "Just execute the changeset with a new family" worked.

# Things that didn't work

I tried a few approaches before reaching the solution. Obviously, they all didn't work or they would be the solution.

1. Just changing family to 14 and executing the changeset -> this doesn't work, as described above.
2. Specifying `DBParameterGroupName` to trigger a complete re-creation of the parameter group. This still triggers the same issue
3. Trying other versions of postgres -- perhaps the issue was that my instance simply didn't support postgres14. This was not the case.

The last option that I didn't bother attempting because it doesn't meet my needs, was to also specify `DBEngineVersion` in the `DBInstance` itself, to force the DBInstance and DBParameterGroup to match. I don't have much faith that this solution would work either.