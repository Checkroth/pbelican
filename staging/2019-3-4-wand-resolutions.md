Title: Dealing with Resolutions in Wand
Date: 2019-03-04
Category: blog
Tags: python, wand, pdf
Slug: wand-resolutions
Authors: Charles Heckroth
Summary: How to handle image resolutions in wand and common pitfalls

Resolutions in wand can be deviously tricky. You might think that it's just an integer (or a tuple), but there are some non-obvious components to this setting.

# Getting the Resolution



```
from wand.image import Image
with Image(filename='myfile.png') as image:
    image.resolution
	
>> (150, 150)
```

# Filetype caviats

# Setting the Resolution

# Changing the Resolution

# Pitfall: Units

# Pitfall: Transformations
