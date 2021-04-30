Title: Professional Open-Source Communication
Date: 2019-08-28
Category: blog
Tags: github, opensource, communication
Slug: prof-os-communication
Authors: Charles Heckroth
<!-- Summary: Communicating politely and effictively with open source maintainers -->

*This blog entry is a work-in-progreses

I recently saw [a tweet that showcased extremely poor communication](https://twitter.com/travisbrown/status/1165502986661105664) in a feature request for an open-source repository. It got me thinking: Sure this person could just be entitled and abrasive, but its more likely he just doesn't know how to communicate well to strangers on github.

I want to break down how I communicate with project maintainers on Github (or whatever version contorl platform you use).

# Basic Guidelines

- Follow the rules for the project or community you want to interract with
    - If a project has rules or an issue template, follow it.
- Don't assume the maintainers will implement your request
    - A lot of projects are dead. Other projects are low priority for maintainers. There's nothing you can do about that.
- Give as much relavent information as you possibly can
    - Outline the problem in detail. Don't make somebody else figure out the problem, because they won't.
- Don't harass anybody
    - I can't believe how many people think Github is an appropriate place to tell people how they are supposed to think. It's not.
- Don't be selfish
    - Do some of the legwork yourself.
- Be friendly, but professional
    - A Please and a Thank You are nice, but keep in mind that you're on a professional and public forum.

# The test case

Let's take the tweet I linked above as a test case. My examples will assume that:

I want the maintainer of a Scala project to publish for a newer version of the language because it is a dependency of another library that uses that version.

What's wrong with the example ticket titled "Publish for Scala 2.13.x please"?

There is basically no information in this ticket other than that the library in question is a dependency to another library.

The title is not in a professional format -- it's a flat imperative request. The author assumes absolutely no responsibility for the request, assuming that asking for it will just be magically done.

The ticket is selfish. The maintainer doesn't care what other libraries that depend on their own do. There's only one dependent listed in the ticket body which really implies that the dependent library should do something about it, not the dependee.

# Opening an Issue

An Issue on Github is how you track the conversation. This is where you make feature requests, report bugs, or inquire about the state of the project. You can open an issue on any repository on github, and this is where you start the conversation.

Many github projects define an issue template with rules and guidelines for how to write a detailed issue. In these cases, you should always follow the template as much as humanly possible. Don't stray from templates, they exist for a reason.

If there isn't an issue template, you should by default include basic necessary information, cleanly formatted.

- The request: "Publish Project for Scala 2.13"
- The reason: "Supporting newer versions of scala allowing newer projects to depend on this library"
- What you've done yourself: Outline what you've actually tried on your own to prove that your first response to an error wasn't to open an issue on Github.
- An example of the reason: "Running a project on Scala 2.13 with Eff will throw <error details>, caused by this project"
- Extra examples if possible: Chances are you aren't the only one with the issue. Find another example to show that you aren't the only one struggling.

# Opening a Pull Request

If possible, you should fork the repository you are opening a ticket to and try to fix the problem yourself. Add a link to your pull request in the ticket. The best way to get a feature implemented in an open source project is to do it yourself.

If you can't fix the code yourself, that's OK. Some issues are complex and outside of your area of expertise. In this case, explain that in the Issue you opened. Let them know that you tried (and what you did), but that you aren't likely to be able to solve it yourself.

If you couldn't fix the issue, you can probably still reproduce the issue. Create a pull request that adds a failing test to the project that shows whatever you're talking about in detail and makes it possible to ensure that if a fix is implemented, it solves the problem.

# Deailing with a dead or low priority project

Some projects aren't very active. Some projects were made by people who aren't around anymore. Maybe they changed careers, or went to prison, or passed away. Or maybe they just don't care about that project enough to work on it anymore.

## Contacting the maintainer

WARNING: Do not contact maintainers who state they do not want to be contacted. As a general rule, only contact them if they have contact info listed _on github_.

You can contact the maintainer of a dead project directly. Give them a nudge to look at your ticket (especially if you've already implemented the fix & opened a PR). If they have no interest in maintaining the project, see if they are willing to transfer ownership of the project to you!

If you do contact them, make sure you've given a reasonable amount of time for them to respond first. DO NOT tweet at a developer as soon as you open a pull request. Wait a week or two before resorting to personal contact. This sort of action can very easily slide over the line in to harrassment. Do not contact them more than once.

I've had success in the past getting pull requests merge by pinging the developer on Twitter. Sometimes they're just not looking. Maybe they're on vacation or something. A notification on a platform they're more actively using is often enough of a push.

## Forking the project

Forking projects is necessary to make a pull request to an open sorce project.

However, if a repository is completely dead with no hope of transfer of ownership, you want to "fork" the repository in to a new project where _you_ are the maintainer.

The standard Fork functionality on github won't do the trick -- this makes your project hidden behind the main, dead repository.

If you want to take ownership of a completely dead project, you need to:

- Keep the same license
- Change the name
- Make it clear that its a fork/copy of the dead repository, and give credit
    - "ThisProject is a library for some feature, forked from OtherProject, a module by SomePerson"

There aren't really "rules" about copying entire projects so you can be the maintainer, but its generally accepted if a project is truly dead as long as you give proper credit.
