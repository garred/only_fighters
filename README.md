# README

A simple game first made in Pygame and later in Godot for the subject _TDDD23 Design and Programming of Computer Games_.

_Only Fighters_ is a 2D top-down action-tactical game, where you control a fighter that kills waves of enemies with different weapons.

Old trailer: https://www.youtube.com/watch?v=IxVr-WvZusE

Android version (pre-alpha): https://play.google.com/store/apps/details?id=org.godotengine.onlyfighters.

The game is still undone and lacks basic functionalities, but it is playable. For now there is no more than three tiny levels, and nothing happens when you finish. In the Python version you could make your own maps with _Tiled_ map editor (http://www.mapeditor.org/), and changing the line in `app.py` where map is loaded to run your map. You can use the existing maps as example. 


## Requirements

- The Python versions uses Python 3, pygame, pgu, PyTMX, pyscroll.
- The Godot version doesn't use anything more.


## Installation

- Python: Just launch `python main.py`.
- Godot: Just load the project and run it.


## Controls

Players can move, punch, slash, roll and pickup things. First player uses arrows, space, and `n`, `m` and `,` keys. Second player (only in Python version for now) uses `w`, `a`, `s`, `d` for direction and shift, `z`, `x`, `c`.


# TDDD23 Game Project Plan "Only fighters"

This game is made as a project for "Design and Programming of Computer Games" course in Linköping University. This section is an early planning of the game, and the game suffered a lot of changes since them.


## Game Idea

The main character (a soldier) fights waves of enemies, with weapons obtained from them, and managing an increasing party of allies. 


### Game style

A 2D top-down action-tactical game, where you control a fighter that kills waves of enemies with different weapons. The weapons are changed frequently (when they are wasted or you lost them while fighting). 

Sometimes there are allies that aren't controlled directly by the player but he can give them general orders like "protect a zone", "come with me", "attack". Their specific behaviour depends on their abilities and equipment. Depending the level and points stored you can choose more members and/or different allies in your party.

There is emphasis in close-combat, where timing is important to hit the enemy and avoid be hitted. Lose a weapon is common, and the characters must fight with their fists or with any reachable weapon.


### Fun

The fun comes mainly from the mechanic of the fight, that involves a micro and a macro level. Micro level is the control of the main character and beating enemies with his various abilities. Macro level consists in managing the strategy and tactics of the party (at a coarse level). Macro level doesn't require as much attention as micro level, and esporadic orders for changing situations may be enough.


### Combat mechanics

Basic combat mechanics are simple, heavily based on the game **Only one**: when you hit, you are unprotected and can't attack again for a little while (like half a second), so you have to be sensible when attacking. You can cancel another character's attack attacking as well (with some exceptions of type paper-scissors-rock). You can use a shield by do nothing, and if you do anything or are looking to a different direction the shield doesn't work and you are hitted.

Some other mechanics are based on the game **Superfighters**: You can punch or you can use a weapon. To use a weapong you have to press the button to "charge it" (like a big sword or hammer) or to aim with it (like a crossbow), and then release the button to attack. The time and precission needed dependes on the weapon. When charging/aiming, the fighter is vulnerable to loss his weapon if someone attack him with his naked hands (punching him). Of course the range of attack is higher using a weapon.

Other mechanics are:

- Dodgin attacks by jumping and rolling when running.
- When receive an attack, loss of control for a little bit. This makes possible to hit repeately the same character, unless he manage to release himself.

Another important thing are the environment. It has physical simulated objects that can be used in the combat (traps with ropes, rocks, explosions...). Maybe some characters (like giants) can throw big objects and hurt throwing them (but usually AI won't use this things).

There are some final bosses and they can be attacked in nearly the same way, with exceptions depending the boss.


### Giving orders

To give an order to an ally, you approach him and a talk button appear. Pushing it, some options are shown and the game pauses. 


### Weapons

To start I think this would be enough: Fists, knife, sword, hammer, bow, spear, shield, gun. Maybe grenade bombs.


### Inspirational games

For game mechanics:

- **Only one**, for Android. The main mechanics and the progression comes from this game.
- **Superfighters**, for web player. Some additional mechanics comes from this game, specially the hand-to-hand combat and the influence of the environment.

For aesthetics and sensation:

- **Flow**, for web player. I love this game. Even if the mechanics is very different, I want that the experience of playing the game to be similar to Flow: smooth dificult curve, slow and fast pace changes, simple and cool aesthetics.
- **Alto**, for Android. Very cool and simple aesthetics, good music, deep experience.
- **NeuroVoider** ([link](http://store.steampowered.com/app/400450/)). Top-down viewed game with simple and good tiled scenaries.
- **Bot Vice** ([link](http://store.steampowered.com/app/491040/)). Same as before.
- **Shadow of the Colossus**, for PS2: Exploration and fighting very well mixed in a game.

For game progression:

- **Transmission** (for Android): Here there are groups of levels grouped by a common element added. The first level of the group is very simple and mainly shows how the new element works. Next levels try the new element with different contexts. Is a good way to learn a new element. 

Things to avoid:

- **The Dungeons of Castle Madness**: [link](http://store.steampowered.com/app/506840/) It has some top-down viewed parts, and they are ugly.
- **Milford Heaven**: [link](http://store.steampowered.com/app/485570/). It is ugly too.


## Game Tech 

KivEnt, a Python framework based on Kivy and Chipmunk2d.


## Progression in the Game

The game evolve modifing this factors:

- Adding more enemies
- Enemies with better AI
- Enemies with different weapons
- Adding more allies in the heroe's party
- Adding some special abilities of the main character.

The expected progression is:

- The game starts with one-vs-one fights with some weapons, allowing the player to get used to the basics of micro level combat. 
- After that, more enemies are added, in different patterns to let the player see how some types of enemies combined are stronger that separated (like an archer with a swordman protecting him). 
- From time to time we can add some situations with physical objects that can be used to solve the level in a different and usually simpler or more interesting way (like exploding or firing a place, flooding it, etc). 
- Then in a normal enemy wave we add some allies. First the simplest type (another swordman). Later we can another or someone of a different type, like a healther, archer, etc.
- Some levels after we can allow the player to choose the combination of characters in his party, before start the level. At the begining of any level there is some info about the probable enemies.


## In-game tutoring approach

Levels are grouped by a common element added. The first level of the group is very simple and mainly shows how the new element works. Next levels uses the new element in different contexts. All groups are ordered by the difficulty of the element (simple weapons first, harder next).

In the firsts missions some message box to guide the player how to move it are allowed: First a message tell to the player how to move the character, later how to attack a dummy objective, after the player is told to dodge attacks from a dumb enemy, how to throw objects and pick up new ones, etc. 

In this missions, there is some neutral and allies units. Give orders to them is as simply as approaching them and clicking the emerging button. This is very intuitive and most players will try it as soon as they see it. If not, a message box can recomend the player doing that.


# CREDITS

Things from other people that I've used so far and don't have its own license:

## Code:

- Phil's pyGame Utilities, https://github.com/parogers/pgu
- `pyganim`, by Al Sweigart al@inventwithpython.com
- `pyscroll`, by bitcraft https://github.com/bitcraft/pyscroll
- Sliding collisions based on code by pymike, http://www.pygame.org/project-Rect+Collision+Response-1061-.html

## Graphics:

- Particles: http://opengameart.org/content/sparks-fire-ice-blood
- Potions: Bonsaiheldin | http://bonsaiheld.org

## Sounds:

- Axe swings: qubodup/Iwan Gabovitch - qubodup.net - qubodup@gmail.com
- Some of these sword swings:
    - afterguard - unionsword 1865 (CC-BY 3.0 -- http://www.freesound.org/people/afterguard/sounds/44660/)
    - black-snow - sword slice 23 (CC-BY 3.0 -- http://www.freesound.org/people/Black%20Snow/sounds/109432/)
    - erdie - sword04 (CC-BY 3.0 -- http://www.freesound.org/people/Erdie/sounds/27858/)
    - jobro - sword pulled 2 (CC-BY 3.0 -- http://www.freesound.org/people/jobro/sounds/74832/)
    - kibibu - sword_4 (CC0 -- http://www.freesound.org/people/kibibu/sounds/22428/)
    - qat - sheath sword (CC0 -- http://www.freesound.org/people/Qat/sounds/107590/)
    - qat - unsheath sword (CC0 -- http://www.freesound.org/people/Qat/sounds/107589/)
    - qubodup - swosh sword swing (CC0 -- http://www.freesound.org/people/qubodup/sounds/59992/)
    - robkinsons - sworddraw (CC-BY 3.0 -- http://www.freesound.org/people/Robkinsons/sounds/103128/)
- "Arg!" sounds:
    - 0: Helmut Scream, http://freesound.org/people/creativeheroes/sounds/84353/, http://creativecommons.org/licenses/by/3.0/
    - 1, 2: Male_Thijs_loud_scream, http://freesound.org/people/thanvannispen/sounds/9432/, http://creativecommons.org/licenses/by/3.0/
    - 3-7: human male scream multi, http://freesound.org/people/JohnsonBrandEditing/sounds/173944/, http://creativecommons.org/publicdomain/zero/1.0/

## Music:

- nene, posted in OpenGameArt.org

## More things

Probably I forgot some things, so if you think I'm using something yours without giving you credit, just tell me and I'll fix it.  
