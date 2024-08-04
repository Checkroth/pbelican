Title: Strava Runmap: A new Pelican Plugin
Date: 2024-08-04
Modified: 2024-08-04
Category: blog
Tags: pelican, python, strava
Slug: launching-strava-runmap
Authors: Charles Heckroth

I lifted a neat activity visualization from my colleague James Van Dyne (with permission), an re-implemented it as a Pelican plugin to mix in with my site, and make it easy for others to do the same.

It can be seen on the [strava runmap section of this site](https://checkroth.com/pages/strava-runmap.html)

# The Visualization

The visualization is a neat thing that my colleague James Van Dyne did [on his Tanzawa Blog](https://jamesvandyne.com/runs/).

It uses the python package [polyline](https://pypi.org/project/polyline/), and takes coordinate data from the [strava api](https://developers.strava.com/docs/reference/) to turn them in to the little line maps.

I have (with permission) lifted this implementation almost entirely as-is from James's [Tanzawa](https://github.com/jamesvandyne/tanzawa). I haven't done any of the heavy lifting myself on these visualizations, just adapted them to my plugin.

# The Plugin

[Strava Runmap](https://github.com/Checkroth/strava-runmap) is a pelican plugin. It has yet to be adopted in to the official [pelican plugins](official). Implementation and configuration details can

There are three main parts:

## 1: Integration with the Strava API

The plugin will, every time you build your pelican site, authenticate with the Strava API and pull every activitity you have ever recorded. It's not particularly performant and will probably slow down your build process.

I only have a few hundred activities (I don't exercise that much and didn't start using Strava until a couple years ago). This process might be unbearable for some users of the plugin, sorry.

## 2: Polyline svg generation

The part explained above. Once we have strava activities, we turn them in to SVGs represented as strings.

These are stored in a context that keeps the svg data and other relevant metadata from Strava, and groups them by year (for display purposes)

## 3: Page Generation

Once we have all the SVGs and related metadata, we generate a full "content" section to include in a pelican page, and inject that page in to the list using a hook in to pelican's pages generator.

The page content is at this moment raw HTML built with a little bit of python. The styles are minimal (primarily flexbox for layout), and are all written in-line, in strings, in python.

# Temporary Usage Until Its Published

It has yet to be published on pypi or adopted in to pelican plugins -- there are a few dangling tasks for the plugin in general. This means it cannot be installed normally as a pelican plugin without a small bit of tinkering:


1. Include the repository as a git submodule in your `plugins` directory.
2. Include the path to the nested repository's plugins directory in your plugin_paths ( `PLUGIN_PATHS = ['plugins', 'plugins/strava-runmap/pelican/plugins']` )
3. Configure the plugin, as instructed in the [readme](https://github.com/Checkroth/strava-runmap/blob/main/README.md)

# What Didn't Work

There were a few things I sort of tried, and failed to find a solution (at least, not one that I was willing to spend the time working on):

1. Not fetching *every* activy - I played around with the idea of keeping some sort of cache, and using that to filter the request to the strava API. I couldn't find out a reliable way to do that filtering or caching, at least not very easily.
2. Storing SVG files as actual static files: I tried to hook in to pelican's staticfiles generator to add the SVGs as actual files, and reference them in the new page. I could not figure out how to pipe raw content in to a staticfile for pelican though -- it crossed my mind to use `tempfiles`, but the context between the tempfile being created and pelican actually trying to access them was also troublesome to deal with.
3. Using real templates: I am building [raw html in python strings](https://github.com/Checkroth/strava-runmap/blob/main/pelican/plugins/strava_runmap/strava_runmap.py#L36) to inject as page content that will eventually be inserted in to a pelican template. I would have preferred for the plugin to define its *own* template and use a more sensible approach, but struggled to find a way to actually do that.

All of the above are certainly *possible*, and maybe even necessary (especially the staticfiles part -- if somebody has thousands of strava actiities, the resulting page might just be too large as a single asset). I am open to contributions directly in strava-runmap :)

# Next Steps

These can be seen in the [issue for incorporating it in pelican plugins](https://github.com/getpelican/pelican-plugins/issues/1405)

1. Fix the build
2. Improve the tests
3. Get adopted as a pelican plugin
4. Publis to pypi
5. Implement a few features we're missing -- like more control over what the page actually looks like, and the ability to include the run contexts in other pages freely for anybody using the plugin.