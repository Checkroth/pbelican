Title: Property Testing: Why You Should Generate Test Data
Date: 2017-08-31
Category: blog
Tags: testing, property testing, python
Slug: property-testing
Authors: Charles Heckroth
Summary: My thoughts on the benefits of property testing

This post is cross-posted to [dev.to](https://dev.to/checkroth/property-testing-why-you-should-generate-test-data)

I drank the functional programming cool-aid at my first _real_ job. While I do not currently professionally develop with functional programming, I still apply what functional concepts I can -- property testing is a big one.

I'm going to cover three main points:
- What's so special about property testing?
- How can I avoid over-complicating my tests when I can't predetermine expected results?
- When _shouldn't_ I use property testing? 

# What's so special about property testing?
Of all the tools available in a functional library, Haskell's _quickcheck_ is the one I see most re-purposed in other non-functional languages.

At first glance, property testing looks like a fancy way of saying "generating test data", and in a sense, it is. So why is it "property" testing?

When you test a function with predetermined parameters, what you're really testing is that the function works for those inputs. You could add a _lot_ of test parameters, enough to cover an "acceptable" range, but that's a lot of unnecessary work and nobody is likely to actually do it (though I have seen it).

When you _property_ test, you don't care what the input is - you're not testing that the function returns some value when given some input. You're testing that the function, when given an argument that fits its requirements (lets say an "int"), will do _something_ and return the appropriate response to whatever input it was given.

Let's look at a very simple example, an adder:
```python
def adder(i1, i2):
  return i1 + i2
```

Simple, it takes two `int`s and returns the sum. That's the property - this function "returns the sum of two ints".

Let's look at a pretty standard test:
```python
class Tests:
  @pytest.mark.parametrize("input1,input2,expect", [(1, 1, 2), (2, 2, 4)])
  def test_adder(self, input1, input2, expect):
    assert adder(input1, input2) == expect
```

This test passes: `2 passed in 0.02 seconds`. We would expect it to - the sum of 1 and 1 is 2, the sum of 2 and 2 is 4. But that's _not what this is testing_.

Let's add some more "adders":
```python
def adder2(i1: int, i2: int):
  if i1 == 1:
    return 2
  if i1 == 2:
    return 4

def adder3(i1: int, i2: int):
  return i1*2
```

And let's run the same test on those:
```python
  @pytest.mark.parametrize("input1,input2,expect", [(1, 1, 2), (2, 2, 4)])
  def test_adder1(self, input1, input2, expect):
    assert adder2(input1, input2) == expect

  @pytest.mark.parametrize("input1,input2,expect", [(1, 1, 2), (2, 2, 4)])
  def test_adder2(self, input1, input2, expect):
    assert adder3(input1, input2) == expect
```

Tests are still passing: ` 6 passed in 0.02 seconds `
Our tests aren't testing the _property_ of this function, only some _explicit_ result for some _explicit_ input.

Now lets take a look at [pytest-quickcheck](https://pypi.python.org/pypi/pytest-quickcheck)
This library gives us a new way of specifying test arguments: `@pytest.mark.randomize`. Let's re-write our first test with it.

```python
    @pytest.mark.randomize(i1=int, i2=int)
    def test_adder(self, i1, i2):
        expect = i1 + i2
        assert adder(i1, i2) == expect
```

Note that I build expect in the test - we can't predetermine the output when we don't know the input.
This test will pass: `9 passed in 0.03 seconds`

Now lets add the rest of the tests:
```python
    @pytest.mark.randomize(i1=int, i2=int)
    def test_adder2(self, i1, i2):
        expect = i1 + i2
        assert adder2(i1, i2) == expect

    @pytest.mark.randomize(i1=int, i2=int)
    def test_adder3(self, i1, i2):
        expect = i1 + i2
        assert adder3(i1, i2) == expect
```

You wouldn't expect these tests to work - adder2 is an if statement and will explode when its first parameter isn't 1 or 2. Adder3 isn't an adder at all - it multiplies.

```
E       assert -4819122279534621102 == -6480923863972990104
E        +  where -4819122279534621102 = adder3(-2409561139767310551, -4071362724205679553)

tests2.py:33: AssertionError
```

Our test is actually testing that our `adder` is _adding_. This might seem like overkill (especially since the test completely re-implements the function), but as you test more complicated functions it begins to make a lot more sense.

# How can I avoid over-complicating my tests when I can't predetermine expected results?

You might consider the "weakness" of property testing to be the fact that you have to write so much _logic_ in your tests - many people turn their noses at the thought! Why should you have to write logic in your tests, especially as they begin to resemble the thing you're testing in the first place?

First, it's actually _okay_ to re-implement your entire function in your test. Especially in a case like adder. The import part is that your test becomes a static part of your project that will do two things: Prove your function works, and prevent you from breaking the function in the future.

A lot of your tests are going to be for more complicated functions - `adder` is an oversimplified example. Let's look at a function that uses more complicated structures.
This function will take a collection of dicts containing x and y coordinates, and calculate statistics for the quadrants of a graph based on where the collection's entries lay.
```python
def calculate_graph_quadrants(entries: List[Dict[Any, Any]]):
    total = len(entries)
    quadrants = {
        'quad1': { 'count': 0 },
        'quad2': { 'count': 0 },
        'quad3': { 'count': 0 },
        'quad4': { 'count': 0 }
    }

    for entry in entries:
        quadrant = calc_quadrant(entry['x'], entry['y'])
        key = 'quad{}'.format(quadrant)
        quadrants[key]['count'] += 1
    for _, quad_stats in quadrants.items():
        quad_stats['share'] = quad_stats['count'] / total
    return quadrants

def calc_quadrant: 
    # takes an x and y, returns quadrant of graph coordinates land
    ...
```
This looks a bit harder to test than `adder` - we have to build this `entries: List[Dict[Any, Any]]`, and somehow determine the expect counts and shares per quadrant. We could generate our data like this:
```python
    @pytest.mark.randomize(xl=list_of(int, items=20),
                           yl=list_of(int, items=20))
    def test_calculate_graph_quadrants(self, xl, xy):
        pass
```
But I wouldn't recommend it - this would require a complete re-implementation of the function. I'm not even going to write what the test would look like because its not worth the effort.

The key to writing a _clean_ property test for a complicated function is to _reduce_ unknowns from your generated data as much as you can without reducing the strength of your test.
```python
    @pytest.mark.randomize(count=int, min_num=1, max_num=50)
    def test_calculate_graph_quadrants(self, count):
        q1 = [{'x': -1, 'y': 1} for _ in range(count)]
        q2 = [{'x': 1, 'y': 1} for _ in range(count)]
        q3 = [{'x': -1, 'y': -1} for _ in range(count)]
        q4 = [{'x': 1, 'y': -1} for _ in range(count)]
        entries = list(itertools.chain(q1, q2, q3, q4)
```
We're not testing the ability to determine what quadrants the coordinates fall in to - that's a different function. We can assume that it works as intended and write another test for that function later.
So all we _really_ need to make variable is how many entries for each quadrant we want to pass to the function. You could make each a different length, but there is little value in that - we can keep our test simple by passing the same amount of data for each expected quadrant.

Since we know how many entries will fall in to each quadrant, the expected result is actually easy to calculate:
```python
    @pytest.mark.randomize(count=int, min_num=1, max_num=50)
    def test_calculate_graph_quadrants(self, count):
        q1 = [{'x': -1, 'y': 1} for _ in range(count)]
        q2 = [{'x': 1, 'y': 1} for _ in range(count)]
        q3 = [{'x': -1, 'y': -1} for _ in range(count)]
        q4 = [{'x': 1, 'y': -1} for _ in range(count)]
        entries = list(itertools.chain(q1, q2, q3, q4)
    # repeat the count for each quadrant, so the total is simple
    total = count*4
    # Each quadrant has the same count - the expected share will also be the same.
    expected_share = count / total
    # we could also do expected_share = .25
    expect = { q: {'count': count, 'share': expected_share}
               for q in ['quad1', 'quad2', 'quad3', 'quad4']}
    assert calculate_graph_quadrants(entries) == expect
```
This test will pass, given that `calc_quadrant` is accurate. That's not too bad, we don't really have that much logic in the test. By controlling what we do and don't want to be randomized, we can determine what our function is supposed to return fairly easily.

_Side note:_ We are all slaves to the limitations of our tools. If we had a library like Scala's `scalacheck`, we would be able to write a generator for `entries` that builds the same thing without writing the logic in our tests.

# When _Shouldn't_ I Use Property Testing?

You should _always_ use property testing. But some libraries aren't cut out for generation on a limited spectrum that you might want. The following could all be done with `scalacheck`'s custom generators, but with `pytest-quickcheck` it simply isn't possible.

Let's demonstrate with a test for `calc_quadrant`. Here's the function:
```python
def calc_quadrant(x: int, y: int):
    if x < 0:
        if y >= 0:
            return 1
        elif y < 0:
            return 3
    if x >= 0:
        if y < 0:
            return 4
        elif y >= 0:
            return 2
```
We could say that this function has four tightly-defined properties, extending from the four logical paths of x and y's sign (+/-). We _could_ randomly generate x and y and build assert like this:
```python
@pytest.mark.randomize(x=int, y=int)
def test_calc_quadrant(self, x: int, y: int):
    if x < 0:
        if y >= 0:
            expect = 1
        elif y < 0:
            expect = 3
    if x >= 0:
        if y < 0:
            expect = 4
        elif y >= 0:
            expect = 2
    assert calc_quadrant(x, y) == expect
```
Look at that, we've just copied the whole function over to the test. I know I said its okay to essentially re-implement your function in your test, but in this case I don't really want to. We can achieve a worthwhile result using `parametrize`, giving all permutations of x and y's signage.
```python
@pytest.mark.parametrize("x,y,expect", [(-1, 1, 1), (1, 1, 2), (-1, -1, 3), (1, -1, 4)])
def test_calc_quadrant(self, x: int, y: int, expect: int):
    assert calc_quadrant(x, y) == expect
```

We still want to use property testing here though, to cover that any range of the test's input will produce an output in our finite range (1-4).

```python
@pytest.mark.randomize(x=int, y=int)
def test_calc_quadrant_in_range(self, x: int, y: int):
    expect_range = [1, 2, 3, 4]
    assert calc_quadrant(x, y) in expect_range
```

This way we can prove that the test will only produce an int corresponding to one of four quadrants. Couple this with the manual quadrant test and we have covered enough of the functionality to make most people happy. Obviously `calc_quadrant` _could_ match specifically for -1 and 1 for our x and y values and otherwise just return `1`, which would satisfy both tests.

Whether or not to implement the former property test (which re-implements the function) is really up to you. I would personally only do that if this were black box testing and I couldn't just look at the code to know that it isn't just matching specific values. Otherwise I would say that manual testing for quadrants and property testing for the result being within range is "close enough".
