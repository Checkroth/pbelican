Title: Rust Implementation of Latin Square Generation
Date: 2022-03-18
Modified: 2022-03-18
Category: blog
Tags: rust, mathematics, prettypileofbones, devlog
Slug: rust-latin-square
Authors: Charles Heckroth

While working on a multiplayer browser game using a rust websocket server, I ran to unexpected difficulty in trying to determine the turn order for a variable sized group of people.

The solution to my issue is a balanced latin square, which allows me to predetermine turn order for my players.

# [The Problem](#the-problem)

The game is a web implementation of an older-than-time-itself group paper game. The game involves drawing on a piece of paper, and then passing that paper to another person, and for that person to continue the drawing.

For the web implementation, I want everybody to always have something to do so that it doesn't get boring. This means that we need as many drawings as we have players. Assuming we have at most as many rounds as we have players, the paper-passing turn order needs to meet the following criteria:

- No drawing can be repated for any player
- No drawing can be repeated in any single round
- Paper-passing should be as random as possible, so that Player 2 isn't always continuing Player 1's drawing, as that would get boring very quickly if you're doing multiple go-arounds.

Consider users A through D, and drawings 1 through 4. Each user should get each drawing once. A fun turn order would be something like the following (each column is a turn of the game, and the # is the ID of the drawing):

```
A | 1 2 4 3 |
B | 2 3 1 4 |
C | 3 4 2 1 |
D | 4 1 3 2 |
```

With this result,

- no user is ever continuing another single user's drawing more than once (diagonal move of number from column to column is never repeated),
- no user is working on the same drawing more than once (rows),
- and no drawing is repeated in any turn (columns)

The name of this structure is a [Latin Square](#latin-squares). Specifically, it is a [Balanced Latin Square](#balanced-latin-squares).

# [Latin Squares](#latin-squares)

Latin squares are matrices of symbols, where each symbol appears exactly once in each row and column.

The above example is one latin square, however they are not necessarily that random. For instance, the following is also a perfectly fine solution:

```
A | 1 2 3 4 |
B | 2 3 4 1 |
C | 3 4 1 2 |
D | 4 1 2 3 |
```

This square just shifts each column one to the right for each row. This satisfies the requirements of the latin square perfectly, however in the context of a game where you are passing these symbols down the line is not ideal.

This would be very boring for player A, since every turn they are continuing a drawing from player B. The same for B with respect to C, C with respect to D, and D with respect to A.


## [Balanced Latin Squares](#balanced-latin-squares)

To maximize interaction between players, by making sure that each player gets to continue the drawing from each other player at least once, we want to implement a **balanced** latin square.

A balanced latin square as seen in [the intro](#the-problem) ensures that on top of being a valid latin square, the shift of a symbol from one row to another is never repeated.

This gives us a solution like

```
A | 1 2 4 3 |
B | 2 3 1 4 |
C | 3 4 2 1 |
D | 4 1 3 2 |
```

However, in the context of the turn orders of a game, there are two glaring issues with this solution:

**1. Balanced latin squares must have an even number of symbols.**

Note the following latin square. There is no solution where each player does not receive from another player two or more times.

There are more sufficient solutions than the following, but it is an example of the mess that happens when you have an odd number:

```
A | 1 2 3 4 5 | receive order: B, E, C, B
B | 2 4 1 5 3 | receive order: D, D, D, C
C | 3 5 4 2 1 | receive order: E, B, E, E
D | 4 1 5 3 2 | receive order: A, C, A, C
E | 5 3 2 1 4 | receive order: C, A, B, A
```

The requirements of the latin square create a sort of deadlock that prevent the beautiful solution of "All rows get a symbol from each potential user".

**2. Latin squares must be even in row and height**

A latin square is an NxN sized grid. In the context of a game, we probably want to allow for configuration for more or fewer rounds.
This means we might want fewer turns than we have players (not a problem), or more turns than we have players (un-balanceable).

## [Nearly balanced Latin Squares](#nearly-balanced-latin-squares)

None of the above issues are actually mathematically solvable. You will always have repeats and holes. For a game, "close enough" is fine, so we want to make *nearly* balanced squares.

### Dealing with odd-numbered grids

The issue with balancing odd number grids is unsolvable.

Most places will state that in order to perfectly balance your odd-number latin square, you have to double the size of the square.

In the context of a game turn order, this really doesn't make any sense. Instead, we just have to break a rule, and add an extra symbol or allow 1 repeat.

- Add 1 to the grid width. Calculate  the `n+1 x n` grid, and lop off the last column.
  - This approach will give you n+1 symbols with no repeats.
- Remove 1 from the grid width. Calculate the `n-1 x n` grid, and then calculate a completely random last row that uses each symbol only once.
  - This approach will give you n symbols with each symbol repeating exactly once. Receive order will also repeat up to n times, once-per-user.

### Deailing with tall grids

```
A | 1 3 2
B | 2 1 4
C | 3 4 1
D | 4 2 3
```

A tall grid cannot meet the requirements of a latin grid, because there are more symbols than there are columns.

The new rules in this case are the same as a regularly balanced latin square. Each symbol should appear exactly once per round. This is easily balanced using the same logic you would use for a regular even-numbered square.

### Dealing with wide grids

```
A | 1   3   2   4?
B | 2   4?  1   3
C | 3   2   4?  1
```

Wide grids are also deceptively simple. It is the inverse of the tall grid.

There are two options from a game perspective: Either include extra symbols so that there is a symbol in every slot, or have only 3 symbols and include passes where the extra symbols would be.

Where a tall grid will have each symbol appear `n=grid_width` times, the wide grid will have each symbol appear `n=grid_height` times. In other words, *in a rectangular grid, each symbol should show up as many times as the shortest grid dimension has entries*.

# [Rust Implementation](#rust-implementation)

With all of the above concidered, perfectly balanced latin squares are mysterious things that simply cannot be easily generated. There are three acceptable approaches for my specific use-case:

1. Limit the number of players and rounds to something reasonable, so that we can just brute-force the solutions
2. Implement Jacobson and Matthews approach, which won't garuntee perfection, but will generate random balanced-ish squares reliably
3. Pre-emptive brute force: Use (1), or (2) with a post-check to see if its balanced, generate as many squares as we can up to reasonable dimensions. Include these as a fixture in the program and randomly select them

For my purposes, I have decided to go with just (2) for now. I may write another post in the future if I decide to expand on it.

The implementation can be found [here](https://github.com/Checkroth/combinatorial_patterns). It is mostly a re-implementation of [Ignacio Gallego Sagastume's C++ implementation](https://github.com/bluemontag/igs-lsgp/blob/master/igs-lsgp/src/jacomatt/model/IncidenceCube.java), though implemented in a way that will hopefully be re-usable. It is [published on crates.io](https://crates.io/crates/combinatorial_patterns).


# [Sources](#sources)

- [Generating uniformly distributed random latin squares, Mark T. Jacobson, Peter Matthews](https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1520-6610(1996)4:6%3C405::AID-JCD3%3E3.0.CO;2-J)
- [Generation of Random Latin Squares Step by Step and Graphically, Ignacio Gallego Sagastume](http://sedici.unlp.edu.ar/bitstream/handle/10915/42155/Documento_completo.pdf?sequence=1)
- [Balanced Latin Square Generator, Damien Masson](https://cs.uwaterloo.ca/~dmasson/tools/latin_square/)
- [A program for making completely balanced Latin Square designs employing a systemic method, Beob Gyun Kim, Taemin Kim](https://www.researchgate.net/publication/262752684_A_program_for_making_completely_balanced_Latin_Square_designs_employing_a_systemic_method)
- [Generating random latin squares, StackOverflow](https://math.stackexchange.com/questions/63131/generate-random-latin-squares)
