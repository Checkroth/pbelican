Title: Dead Tuples and Poor Postgres Performance
Date: 2022-04-06
Modified: 2022-04-06
Category: blog
Tags: postgres, databases
Slug: postgres-garbage
Authors: Charles Heckroth
status: draft

On a project I work on, we frequently struggled with painfully slow queries (tens of seconds to several minutes). The queries were pretty big (aggregation and joins across 10s of tables, some of which with hundreds of thousands of records). Try as we might, we couldn't speed them up.

At one point it got so bad (through a series of misguided implementation choices) that I took down our production environment by eating up all the available connections on our postgrse instance (many untenably slow queries running in unison with no end in sight).

Ultimately, we were able to reduce query times from ~30+ seconds to ~20ms by manually running garbage collection. Which we really shouldn't need to do. This post is going to talk about

- The origin of the problem
- The long-term solution
- The lessons learned / things to look out for so it doesn't happen again


# The Problem

# The Solution

# How to make my stuff work more good