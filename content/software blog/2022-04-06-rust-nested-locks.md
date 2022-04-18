Title: Nested Arc RwLocks in Rust
Date: 2022-04-18
Modified: 2022-04-18
Category: blog
Tags: rust, prettypileofbones, devlog
Slug: rust-nested-rwlock
Authors: Charles Heckroth

In my attempt to create what amounts to an in-memory database in rust for a game project, I ran in to a topic for which I could find no explicit documentation.

"Can I nest RWLocks, read the inner lock out of the outer lock, and then read/write the inner lock without maintaing the read lock on the outer lock?"


# The Details

My architecture involves a single endpoint websocket server, which takes a "game type" and a "session ID" parameter.
Each game type has a RWLock hashmap of individual game information. This is essentially a "GameType" table.

I want to take the game type and session ID and read the individual instance of the game, and forward that game to a thread which will take read/write locks as required when receiving messages through the websocket.

We need several people to be able to hold a reference to the inner game lock at a time, while still permitting other people to create new games of either type. So ten people may or may not be holding a read/write lock on an instance of the inner lock, which should have no impact on whether or not other people can read/write from the outer lock.

This is the general structure:

```rust
struct TypeA {}
struct TypeB {}

struct Sessions {
    type_a_sessions: Arc<RwLock<HashMap<usize, Arc<RwLock<TypeASession>>>>>,
    type_b_sessions: Arc<RwLock<HashMap<usize, Arc<RwLock<TypeBSession>>>>>,
}
```

Container -> outerlock -> hashmap -> innerlock -> session

And what I would like to do with this looks something like the following:

```rust
    // ws_rx: futures_util::stream::SplitStream<warp::ws::WebSocket>
    while let Some(result) = ws_rx.next().await {
        let msg = match result {
            Ok(msg) => msg,
            Err(e) => {
                break;
            }
        };
        if let Some(game) = game_sessions.read().await.get_mut(&user_args.session_id) {
            // The inner game should be able to be processed indefinitely, without holding a lock on `game_sessions`
            user_message(&user_args, msg, game).await;
        }
    }
```

# The Solution

Is incredibly straightforward.

The answer is simply that yes, you can nest locks. You can drop the outer read or write lock after assigning the inner lock value to a variable in a wider scope, and operate on the inner variable safely.

## The Code

This is just the raw playground example I came up with. It will comipile in the rust playground but may time out, so if you want to run it you should probably do it locally.

There is a handy trick here which might be new to rust beginners. Within `read_outer`, I define `inner_lock` and `inner_lock2` with a type and no value. I then start a new block inside of some unlabaled braces. Anything declared within those braces is scoped to within those braces.

So, `inner_lock` and `inner_lock2` are defined outside the braces so that they will  persist, and `rlock`, defined inside the braces, will be dropped.

```rust
use std::sync::Arc;
use tokio::sync::{RwLock};
use std::collections::HashMap;

#[derive(Default, Debug)]
struct Inner {
    pub incremented_count: usize
}

type InnerLock = Arc<RwLock<Inner>>;
type LockedMap = Arc<RwLock<HashMap<usize, InnerLock>>>;

#[tokio::main]
async fn main() {
    let inner_map: HashMap<usize, Arc<RwLock<Inner>>> = HashMap::from([
        (1, InnerLock::default()),
        (2, InnerLock::default())
    ]);
    let map = LockedMap::new(RwLock::new(inner_map));
    read_outer(map).await;
}

// Reads an instance from the outer lock, releases the outer lock,
// and then passes the inner lock to another function
async fn read_outer(map: LockedMap) {
    println!("Inner!");
    let inner_lock: InnerLock;
    let inner_lock2: InnerLock;
    {
        // Fetch inner lock twice and then lose the write lock on the outer structure
        // This is to verify that:
        // 1: rwlock can still be accessed even if its nesetd inside another, and the outer is lost
        // 2: The rwlock still references the same information -- I can update inner_lock,'
        //  then read the new value from inner_lock2, then read from the outer lock again
        let rlock = map.write().await;
        let i: usize = 1;
        inner_lock = rlock.get(&i).unwrap().clone();
        inner_lock2 = rlock.get(&i).unwrap().clone();
    }
    let expect1 = 0;
    let (_, _) = tokio::join!(
        read_inner(&inner_lock, expect1),
        read_inner(&inner_lock, expect1)
    );
    write_inner(&inner_lock2).await;
    let expect2 = 1;
    let (_, _) =tokio::join!(
        read_inner(&inner_lock, expect2),
        read_inner(&inner_lock2, expect2)
    );
    let expect3 = 2;
    write_inner(&inner_lock).await;
    let (_, _) =tokio::join!(
        read_inner(&inner_lock, expect3),
        read_inner(&inner_lock2, expect3)
    );
}

// Reads the value from an inner lock
async fn read_inner(inner: &InnerLock, expect: usize) {
    let readlock = inner.read().await;
    assert_eq!(readlock.incremented_count, expect);
    println!("Inner value was {}", expect);
}

// Writes a new value to the inner lock.
// Same lock should be read by a different thread, both this and the other having released the read lock on outer.
async fn write_inner(inner: &InnerLock) {
    let mut writelock = inner.write().await;
    writelock.incremented_count += 1;
    println!("Inner value changing from {} to {}", writelock.incremented_count, writelock.incremented_count + 1)
}


```