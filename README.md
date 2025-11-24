# The JAB(R)
The JAB(R) is a combination of Jasper, Alexandro Donophrio, Ben, and Rowan. It is a present-catcher game with rigged winnings to ensure maximum profit - a bit like a carnival game, except we can guarantee our winnings.

## List of Modules

| **Module Name** | **Module Type** | **Description** | **Merged in *30d9811***
| ----------- | ----------- | ----------- | ----------- |
| JSONHelper  | Helper Module | Has 'read' and 'write' functions to read and write from JSON files given a path. | ✅ |
| ImageHelper | Helper Module | Has functions for working with images in pygame (e.g. load_spritesheet_images, generate_hitbox) | ✅ |
| Compadre | Primary Module | Main module for rigging the game. Stores/saves data on current game status and [TODO] has functions to provide speeds & positions of unreachable presents. | ❌ |
| Globals | Game Module | Stores constant-return functions and variables to be accessed from other files. (e.g. win) | ❌ |
| Classes | Game Module | Stores frequently-used classes to do with the game's functions. Some helper classes may have seperate classes. | ✅ |

## Compadre
Compadre's task is to assist with rigging the game, currently saving and loading given data into a file storing the game's current state, and whether it should provide a rigged output or not.

The file's format is: 'FCN'. `Flag`, which dictates whether rigging should currently be available. If False, then the game is rigged, if True, then the player can win. When `Flag` is True, the state cannot be reset until a round is won. This ensures the game is not too hard to beat. `Current Try (C)` is the value of whatever try the game is currently on, also referred to as the current round. `Next Try (N)` tells Compadre which try (round) the rigging should be disabled for. `Flag` still exists in this circumstance due to the fact that `Flag`'s state is locked at True until a round is won, thus the player could have a `Current Try` of 4 if they haven't beat the game twice since the `Next Try` at 2.

Compadre uses hexadecimal encoding (with the `struct` module) to store this data as efficiently as possible. This means that the data is only 3 bytes large, appears like spaces when viewed in notepad, and is still just as effective, not  losing any data. The data for the values of `Flag`, `Current Try`, and `Next Try` are all unsigned characters ('B'). This means they have an upper limit of 255, and cannot be negative.

### writeCompadre(currentTry: int, triesToReset: int)
*Writes the current information to Compadre. Use this for rigging.*

```py
import compadre

compadre.writeCompadre(4, 10)
# .jab - \x010404 | \z0004??
```

**Known Issues**
* Writing to Compadre expects to reset nextTry

### readCompadre()
*Reads the current information stored and relays it back to you!*

```py
import compadre

print(str(compadre.readCompadre()))
# {"flag": True, "currentTry": 4, "nextTry": 4}
```

**Known Issues**
* ?