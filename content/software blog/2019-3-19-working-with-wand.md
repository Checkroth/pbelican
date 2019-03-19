Title: Working with ImageMagick's Wand Python Library
Date: 2019-03-19
Category: blog
Tags: python, python-wand, pdf
Slug: wand-resolutions
Authors: Charles Heckroth
Summary: Handling Wand Resolutions, Units, and Image Types

Handling images in wand can be deviously tricky, especially when you need a common system-wide resolution.

An example use-case:

I work on a system that sends & receives faxes. It also handles email attachments and draws text on to fixed format images (inquiries, order details, etc.).

Due to the fact that we're writing in to fixed formats with wand, and also writing on top of faxes and sending faxes (through Twilio), a system-wide fixed resolution makes things a lot easier.

I frequently experience issues with font and draw position scaling, particularly when writing on PDFs.

When I reference `pdf.pdf`, I am specifically referencing [this document](http://www.pdf995.com/samples/pdf.pdf).

# Getting the Resolution

An image file has some resolution metadata attached to it.

```python
from wand.image import Image
with Image(filename='myfile.png') as image:
    image.resolution
	
>> (150, 150)
```

You can also specify a resolution when opening it in Wand, and it will scale it for you


```python
from wand.image import Image
with Image(filename='myfile.png', resolution=200) as image:
    image.resolution
	
>> (200, 200)
```

This works fine for regular images, but it's a bit tricky with PDFs.

# Dealing with PDFs

## PDF Resolutions

The first thing to note with a PDF is that wand will _not_ open it in its original resolution.

```python
with Image(filename='pdf.pdf') as image:
    image.resolution
>> (72, 72)
```

A PDF opened in wand will always be at a resolution of 72. A PDF _created_ in wand will _also_ always have a resolution of 72. If you want to do any remotely complex image processing on a PDF with Wand, you must always specify a resolution or you will run in to a lot of issues. The biggest being that every time you open and save the PDF, its quality will reduce dramatically (if its original resolution was greater than the default 72).

```python
with Image(filename='pdf.pdf', resolution=200) as image:
    image.resolution
>> (200, 200)
```

Specifying the resolution when opening the pdf will work as expected.

Creating a new pdf works the same, which can actually be quite confusing.

## Wand-created PDF Resolutions

Say you want to create a new PDF. You want it to be in Letter size, so you program assuming the PDF is at the default resolution, and then scale all of your widths, heights, and coordinates up to your system-wide resolution.

```python
with Image(width=500, height=500) as image:
    image.save(filename='test_pdf.pdf')

with Image(filename='test_pdf.pdf', resolution=200) as i:
    i.width, i.height

>> (1389, 1389)
```

If you're scaling your sizes and positions when creating your pdf, re-opening at the resolution you have specified is going to explode its size significantly.

```python
with Image(width=500, height=500) as image:
    image.resolution = 200
    image.save(filename='test_pdf.pdf')
	

with Image(filename='test_pdf.pdf', resolution=200):
    i.width, i.height

>> (500, 500)
```

It is important to specify the resolution _before_ saving the PDF or doing any drawing operations.

It is also important to note that creating a new PDF at a certain resolution will _not_ work if you pass the resolution in the constructor. I'm not really sure why, but the above code will work while `Image(width=500, height=500, resolution=200)` will reproduce the original resolution explosion issue.

# Image Units

Wand has three units of measurement.

- `undefined`
- `pixelsperinch`
- `pixelspercentimeter`

PDFs are undefined by default. They don't hold the metadata like a `png`, `tiff`, etc. What `undefined` means is determined by ImageMagick itself, which probably references something in the operating system.

In my personal experience, `undefined` has always calculated as `pixelsperinch`, but it may be different on other operating systems or environments. It's best to specify a system-wide unit and use it whenever you open an image.

## Magic Units

I used magic units for some time (leaving everything as `undefined`). Then one day, we decided to change our Twilio settings to send us images as Tiffs instead of PDFs.

As it turns out, Tiff actually has the unit metadata, and it was set to `pixelspercentimeter`. Everything we received after that change was completely incorrectly processed because we had until that point processed everything as `undefined` or `pixelsperinch`.

# Pitfall: Resizing

Resizing very handy. Especially in the previous example of receiving Tiffs from Twilio.

A fun side-note: Faxes can be sent with different quality levels: Normal, Fine, and Superfine. These qualities actually only increase the vertical axis. When twilio sends you a PDF it transforms it to its intended aspect ratio for you, but a Tiff is the raw data. Normal will be flag, Fine will be the right ratio, and Superfine will be incredibly tall.

To deal with this, I had to resize the Tiff before saving it so we could process it normally. For instance, for a `normal` quality fax:

```python
with Image(filename='received.tiff) as image:
    image.resize(image.width * 2, image.height)
	image.save(filename='resized_image.tiff')
```

The problem here is that resizing an image in wand has no impact on its resolution.

Meaning, if you had a resolution of `(100, 200)` and resized it as specified above, the resolution will not become `(200, 200)`, but remain the same. Then the next time you open it, things are going to get _really weird_.

```python
with Image(filename='received.tiff) as image:
    image.resize(image.width * 2, image.height)
	image.resolution = (image.resolution[0] * 2, image.resolution[1])
	image.save(filename='resized_image.tiff')
```

would appropriately resize the image and its resolution.

# Pitfall: Sequences

Wand drawings aren't exactly meant for PDFs or layered images. Neither is the resize utility, or really anything else.

Wand images have a `sequence` attribute, which is crucial.

You might think that if you do `draw(image)` with wand, you would write on the first page of the PDF. It will draw it on the last page.

Wand has an `index_context` to deal with this:

```python
# assuming your draw attribute is created already
with Image(filename='pdf.pdf') as image:
    with image.sequence.index_context(0):
	    draw(image)
```

This will draw on the first page. Changing the integer you pass in to index_context will change the page you draw on, just like any iterable in python (or any other language).

# Pitfall: Coding for Low Resolutions and Scaling Up

When I started out, I coded all of my text-writing-on-pdf stuff with the default resolution, because I didn't really understand anything I've written up to this point (it was a learning process.)

Wand hates floats and doubles. Font sizes, positions, widths, heights, and everything else is restricted to integers.

If you program pdf writing assuming the resolution is 72 and then scale up, the higher you go the more off things are going to be. If you start high and go low, things will be a lot more accurate.

72 is in general way too low quality for PDF processing and you'll probably be using at least 150 or 200, so you should probably start out the gate assuming your pdfs are that resolution to avoid rounding errors.

# Pitfall: Colorspaces

You can't write on a CMYK colorspace. If you try, you'll write on a different layer. White will become black and black will become white, and other things will become other things. It's a huge headache.

My advice is to turn around and quit as soon as you see CMYK, but that's obviously not an option all the time.

To deal with CMYK, the best you can do is something like this:


```python
with Image(filename='cmyk_pdf.pdf') as image:
    original_colorspace = image.colorspace
	if original_colorspace = 'cmyk':
	    with image.sequence.index_context(0):  # or whatever page / pages you're processing
		    image.transform_colorspace('srgb')
	draw(image)  # do all your drawing now
	image.transform_colorspace(original_colorspace)
	image.save('cmyk_drawn_pdf.pdf')
```

You'll probably still encounter some issues, but if you're going to draw on a cmyk pdf this is the best solution I've come up with.


# Pitfall: Wand Scope

Wand eats your memory. All of my code examples have `with Image() as image):` to keep the image file in context.

If you do `i = Image()`, then you need to call `i.close()` when you're done with it.

If you're working on a large system, its best to avoid passing around Image instances and to localize it all to one module.

Colors, Drawings, and all other Wand objects should also be handled within a `with` context.


# Notes

1: I am not primarily an engineer who deals with images, so some of my understanding could be wrong (the code works,  but the underlying reasons could be different from my current understanding)


2: I mention scaling a few times. 

I generally scale positions and sizes with `math.floor(value * (SYSTEM_RESOLUTION / IMPLEMENTATION_RESOLUTION))`, where `SYSTEM_RESOLUTION` is the resolution you want, `IMPLEMENTATION_RESOLUTION` is whatever resolution you assumed when writing the code, and `value` is the value you want to scale.

3: Making an new image: I generally call this a `canvas`, and its important to specify the background color if you're going to be creating some sort of business document with the `background` parameter to the `Image` constructor.

4: Wand uses ImageMagick to process everything, so outside of the wand version (I'm using `0.4.4`), your operating system and ImageMagick version could also make things work differently.
