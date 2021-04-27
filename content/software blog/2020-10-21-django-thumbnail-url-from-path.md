Title: Django Easy Thumbnailer URLs from Filepaths
Date: 2020-10-21
Category: blog
Tags: python, django, filestorage
Slug: easy-thumbnails-from-path
Authors: Charles Heckroth
Summary: Forcing easy_thumbnails to calculate a URL without a direct object reference
Status: Draft

# The Problem

[easy_thumbnails](https://github.com/SmileyChris/easy-thumbnails) is a handy library for automatically resizing & storing various sizes of an image. As the name implies, it is an easy way to create thumbnails for images in your django project so you don't have to use massive original-size images for tiny thumbnail displays.

It does however come with its problems, particularly with the amount of queries it executes. It's handy for processing single instances, but when you have a list of hundreds of objects the use of easy\_thumbnail's template filters is going to throw out _a lot_ of unnecessary queries. At least one, often more than one, for every object. This is going to make page rendering painfully slow, so it should be avoided.

In django you would generally avoid this by using features like `prefetch_related` and `values_list` to get the information you need in one go, but you can't use easy_thumbnail's features with these standard Django ORM functions. 

So if you want to get a list of the urls for a thumbnail size for a model, given a model like:

```python
class MyModel(models.Model):
    image = ThumbnailerImageField(upload_to="images/")
```

You would have to get your thumbanils like this:

```python
thumbnails = [get_thumbnailer(x.image)['mysize'].rul for x in MyModel.objects.all()]
```

But that's going to execute a query for every object and is no better than just using the built-in template filter.

And `MyModel.objects.values_list('image', flat=True)` is only going to give you the name of each image -- not the object you need for using easy_thumbnails `get_thumbnailer`.

So *how can we get a list of thumbnail URLs*?

# The Solution

To get a list of thumbnail urls without executing a query for each instance of your object, you need to trick easy_thumbnails in to _thinking_ it has an instance of each object, when really you just have a list of file names.

```python
from easy_thumbnails.files import ThumbnailerImageFieldFile
from easy_thumbnails.files import get_thumbnailer

throwaway_object = MyModel()

thumbnails = (get_thumbnailer(ThumbnailerImageFieldFile(instance=throwaway_object, field=throwaway_object.image.field, filename))['size'].url
              for filename in MyObject.objects.values_list('image', flat=True))
```

