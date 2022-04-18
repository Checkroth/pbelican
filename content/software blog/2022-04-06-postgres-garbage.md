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

The surface level problem is obviously that our tables are big and bloated, filled with god knows what data from years ago.

The real issue however is that postgres *should* be cleaning this up itself, and it isn't. But *why*?

# The Solution

Occasionally running manual the postgres analyzer and vacuum by hand is *not* a solution.
The long term solution is to fix whatever was preventing these things from running on their own. We never messed with our postgres configuration, and by default it should be regularly cleaning this stuff up on its own.



# How to make my stuff work more good

# Sources

- [Reasons Why Vacuum Won't Remove Dead Code, Laurenz Albe, cybertec-postgresql](https://www.cybertec-postgresql.com/en/reasons-why-vacuum-wont-remove-dead-rows/)
- [Stale Statistics Cause Table Bloat, Laurenz Albe, cybertec-postgresql](https://www.cybertec-postgresql.com/en/stale-statistics-cause-table-bloat/)
- [Understanding Autovacuum in Amazon RDS for Postgresql Environments, Anuraag Deekonda and Baji Shaik, aws](https://aws.amazon.com/blogs/database/understanding-autovacuum-in-amazon-rds-for-postgresql-environments/)
- [Trouble with Autoanalyze, Tomas Vondra, 2ndquadrant](https://www.2ndquadrant.com/en/blog/when-autovacuum-does-not-vacuum/)
- [](https://www.2ndquadrant.com/en/blog/autovacuum-tuning-basics/)