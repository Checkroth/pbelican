Title: Nested Arc RwLocks in Rust
Date: 2022-04-06
Modified: 2022-04-06
Category: blog
Tags: rust, prettypileofbones, devlog
Slug: rust-nested-rwlock
Authors: Charles Heckroth
status: draft

In my attempt to create what amounts to an in-memory database in rust for a game project, I ran in to a topic for which I could find no explicit documentation.

The primary question I tend to answer in this post is:

"Can I nest RWLocks, read the inner lock out of the outer lock, and then read/write the inner lock without maintaing the read lock on the outer lock?"

# The Details

My architecture involves a single endpoint websocket server, which takes a "game type" and a "session ID" parameter.
Each game type has a RWLock hashmap of individual game information. This is essentially a "GameType" table.

I want to take the game type and session ID and read the individual instance of the game, and forawrd that game to a thread which will take read/write locks as required when receiving messages through the websocket.

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

And what I would like to do with this looks something like

```rust
    // ws_rx: futures_util::stream::SplitStream<warp::ws::WebSocket>
    while let Some(result) = ws_rx.next().await {
        let msg = match result {
            Ok(msg) => msg,
            Err(e) => {
                break;
            }
        };
        // TODO:: change this bit to look up type_a|b_sessions via read lock
        if let Some(game) = game_sessions.write().await.get_mut(&user_args.session_id) {
            user_message(&user_args, msg, game).await;
        }
    }
```

# The Solution