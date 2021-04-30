Title: Roping in Complexity, Decay, and Duplication in a Growing Scala Project
Date: 2016-09-13
Category: blog
Tags: scala, conference, scalamatsuri
Slug: 2017-scala-matsuri-cfp
Authors: Charles Heckroth
<!-- Summary: This was my (unaccepted) proposal to Scala Matsuri 2017. -->

# Roping in Complexity, Decay, and Duplication in a Growing Scala Project

All software projects will grow in complexity and decay over time. 
[Lehman's Laws](https://en.wikipedia.org/wiki/Lehman's_laws_of_software_evolution) of software evolution state that as a system evolves, "its complexity increases unless work is done to maintain or reduce it", and that a system "must be continually adapted or it becomes progressively less satisfactory".

Scala has a lot of tools to help combat complexity and decay. I will cover my own process of spotting decaying components of our system, and how my team and I apply functional programming concepts to grow our system without wide-spread, unmaintainable complexity growth.
Specifically, how we define and practice standards within our group of engineers and how I utilized Shapeless and HLists to remove heavy code duplication.

I will briefly touch on the following specific topics:
- Scalaz and Functional Syntax as a standard
- Code formatting with Scalafmt
- Common structures vs. Copied Code
- Doing it right the first time
- Removing duplicated code using Shapeless
