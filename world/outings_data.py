"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Outings scenarios and effects.
"""

OUTINGS = {
    "Plains": {
        "enemy camp": (
            {  # 1
                "name": "Car Column",
                "type": "Enemy Camp",
                "class_weights": {"soldier": 15, "raider": 4, "anarchist": 7},
                "assignees": 3,
                "day_part_weights": {
                    "night": 10,
                    "morning": 0,
                    "noon": 3,
                    "evening": 8,
                },
                "desc": """You're catching your eyes on four big black jeeps, standing in a row.
They are covered with dust, but even from that big distance you can
say they are in a good shape. No human around makes it tempting to
send some folks to recon the place - is your first thought. But when
the Train engine finally falls silent, you're hearing voices, flying
from the car column side. Definitely, there are people somewhere
there, still, it's not possible to see them from your spot. So, the
initiative becomes little bit risky. It's worth it to send three of
your fighters together to check the cars.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """{name1}, {name2} and {name3} are jumping off the Train, and
taking a direction to the jeep column. Holding closer together, they
are silently moving from one tree to another, smoothly approaching
to the cars. In some moment you understand that voices, which were
flying to you from the column, vanished. Something is wrong! You're
finding your people by your gaze, and in this moment a machine gun
shots tearing the air. Your whole team starts to shoot back, slowly
crawling back to the Train, as the enemy seems to be full of ammo.
You're trying to help others with your fire, and the rival shots are
starting to fly to the Train. Taking cover, you're waiting for {name1},
{name2} and {name3} to return and giving the order to start the engine.
Train getting -80 damnability""",
                        "effects": {"train": {"damnability": -80}},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """{name1}, {name2} and {name3} are taking the direction to the jeeps
by your command. They are moving across the meadow silently for
some time, but suddenly a sturdy with a machine gun appears near one of
the jeeps and starts to shoot at your people, pinning them to the ground.
You're seeing {name3} showing something to others by {hisher3} hand.
{name1} and {name2} turn around and move back to the Train, while {name3}
covering them with aggressive fire. The sturdy, experiencing a bullets
storm, hides behind the car. {name1} and {name2} closing to the Train and
taking a turn around to cover {name3} retreat. Hearing a short pause,
sturdy appears back behind the car and shoots to {name3}, but {heshe3}
returns back to the Train with just a couple of small wounds.
{name3} getting -25 health
{name1} and {name2} getting -15 health""",
                        "effects": {
                            "char_1": {"health": -15},
                            "char_2": {"health": -15},
                            "char_3": {"health": -25},
                        },
                    },
                    {
                        "score": range(40, 60),
                        "desc": """{name1}, {name2} and {name3} jumping off the Train and moving
to the jeeps column. You're seeing them silently approaching the cars.
Hopes, there is no one around... Not even throwing a look inside the
cars, your people are simultaneously turning around and running back
to the Train with the full speed. You're taking your gun, preparing for
the fight. But no one follows your messengers, so you only have to wait
them. {name2} climbing the Train back first. "There are at least fifteen
people, lower, near the river." - {heshe2} explains, breathing heavily.
You nod your head and giving the command to warm up the engine.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """You're sending {name1}, {name2} and {name3} for a short
recon of the place. Your teammates are moving to the jeep column,
while you track them from the Train; seeing how {name2} opens a car,
and starts to rummage in the glove compartment. Suddenly, you hear
cries, but not of your messengers. Still, they are reacting fast, and
turning around back to the Train. Looks like there was someone there!
Confirming this, several naked people appearing near the jeeps. But
to the moment they grabbed their guns and started to shoot, {name1},
{name2} and {name3} are jumping onto the Train. "No empty hands!"
- {name2} proclaims and shows dollars on {hisher2} palm.
You're getting +80$""",
                        "effects": {"money": 80},
                    },
                    {
                        "score": range(80, 100),
                        "desc": """{name1}, {name2} and {name3} are taking the direction to the jeeps
column. {name2} and {name3} are opening two of the cars at once,
while {name1} stands on the watch. You're seeing {name2} grabbing a
canister from the car inners. With this find {heshe2} without stops moves
back to the Train. {name3} in the next few seconds rummages the jeep,
but in some moment {name1} jumps on {hisher1} place and starts to
shoot to somewhere behind the column. {name3} grabs the first thing
{heshe3} see and turns to the Train. {name1} takes few more seconds
to shoot at those on the other side, but they fight back tough, so
{heshe1} has to retreat. Returning fast, your people show the catch.
You're getting +90$ and 1 stimulator
{name1} getting -15 health""",
                        "effects": {
                            "money": 90,
                            "stimulators": 1,
                            "char_1": {"health": -15},
                        },
                    },
                ),
            },
            {  # 2
                "name": "Big Tent",
                "type": "Enemy Camp",
                "class_weights": {"soldier": 45, "raider": 20, "anarchist": 9},
                "assignees": 1,
                "day_part_weights": {
                    "night": 0,
                    "morning": 10,
                    "noon": 6,
                    "evening": 4,
                },
                "desc": """It takes not less than ten seconds for you to understand is something
there, or it's just a big bush. Yes, something is definitely there - a square
dark green tent, very similar to a soldier's one. It doesn't look like there
are people in there, but the tent is still standing, so most likely someone
cares about it. The maximum number of sleepers in such a tent equals to
four, and they should have to hear the Train approaching. No signs of
movement means no human, right? It's little bit dangerous, but makes
sense to send someone to check if anything useful lies in this tent.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You're ordering {name1} to move closer to the tent and take a
look at it. {name1} jumps off the Train and runs fast to the spot.
You're tracking {himher1} from the cabin, staying sharp. Approaching
the tent closer {name1} slows down little by little, but in some
moment {heshe1} suddenly grabs {hisher1} leg and falls on the ground. You
jump out of the cabin and bring binoculars to your eyes. No one
appeared anywhere, so you're catching a breath and taking a more
careful look at {name1}. It seems like {heshe1} failed into a trap.
You're moving binoculars away and, jumping down to the ground,
take direction to {name1} to help {himher1} to get out.
{name1} getting -25 health""",
                        "effects": {"char_1": {"health": -25}},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """{name1} takes {hisher1} gear and heads to the tent by your command.
You're staying on the Train on the watch, holding your gun with
one hand. {name1} cautiously moves through the green meadow to the
tent, and once the tent starts to swing. You're throwing up your gun
and taking the spot on the sight. An old man jumps out of it and,
turning a big shotgun onto {name1}, thunders the air with a shot.
As the distance between {name1} and the shooter is too long for a
shotgun, it most likely was a warning shot. In the next moment the old
man sees you and the Train, and he freezes. "{name1}, get back!" -
you're shouting, and {heshe1} starts to move to the Train back forward.
The old man continue to hold his gun up, but he don't shoot any more.
"He got me a little" - {name1} climbs up on the Train and shows
{hisher1} bloody shoulder. {name1} getting -10 health""",
                        "effects": {"char_1": {"health": -10}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """You're sending {name1} to take a closer look at the tent. {name1}
takes {hisher1} gun and fastly moves to the place. The meadow smells
with flowers and dust, grasshoppers are jumping all around, and there
is no any single sign of a human. No garbage, no crumpled grass, no
defensive traps. Getting closer to the tent, {name1} sees that it's full
of shot holes. No doubts, someone crept up to it and shoot away all who
was inside. Not very nobly. {name1} accurately moves to the tent entrance
and takes a look into it. Several skeletons in soldiers uniform, and no
guns, supplies or anything useful at all. Someone already looted the
place clean. In disappointed mood {name1} returns back to the Train.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """By your command, {name1} gears up and takes a direction to
the square tent. First half of {hisher1} way {heshe1} runs fast, but then
{name1} slows down hard, carefully looking under {hisher1} feet. You're
staying sharp as it looks like there are traps there, and where traps
- there people, who set them. Still, {name1} approaching the tent
without any sign of a trouble. Taking an accurate look inside, {heshe1}
disappears in the tent inners. You're feeling little bit nervous, but
several minutes passes, and {name1} walks out on the meadow. Carefully
choosing the steps, {heshe1} returns back to the Train and shakes a
bunch of dollars in {hisher1} left hand, showing it to you.
You're getting +50$""",
                        "effects": {"money": 50},
                    },
                    {
                        "score": range(80, 100),
                        "desc": """You're sending {name1} for a small recon. Taking {hisher1} gun,
{heshe1} moves fast to the tent, while you're tracking {hisher1} movement
through the binoculars. At a few seconds {heshe1} closes to the spot from the
side, and suddenly tissue entrance of the tent flyes up with loud gun
shots. {name1} lighting fast ups {hisher1} gun and makes several shots. Silence
falls on the meadow... {name1} carefully taking a look inside the tent and
enters it. In the next second {heshe1} jumps out of it and runs back to the
Train. "Skinhead scum!" - {heshe1} says, entering the Train cabin. - "Seems
like he tried to shot me before he actually saw me. Missed." - {heshe1} adds,
pointedly putting several banknotes onto the table.
You're getting +90$""",
                        "effects": {"money": 90},
                    },
                ),
            },
            {  # 3
                "name": "Bus",
                "type": "Enemy Camp",
                "class_weights": {"soldier": 22.5, "raider": 6, "anarchist": 14},
                "assignees": 2,
                "day_part_weights": {
                    "night": 0,
                    "morning": 3,
                    "noon": 10,
                    "evening": 7,
                },
                "desc": """The big red two-storied bus standing at the middle of the meadow
catches your attention from a very long distance. Bringing the binoculars
to your eyes you're seeing that it's little bit old and shabby, but sand
bags and logs placed around the car in defensive positions tells it's
still inhabited. You also see that second floor doesn't have any glass
in windows - probably a sniper point, but, except this fact, the
bus seems to be safe. That makes sense to send a couple of people
to check if there is something valuable in there.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You're sending {name1} and {name2} to take a look at the bus.
Moving to the car they are looking around carefully. The meadow is
visible for three hundreds meters around, and nothing promises troubles,
so after a couple of minutes of walk they relax. In that moment a shot
thunders in the air. Sniper! You're seeing his long gun barrel protruding
from the empty window on a second floor. Another shot thunders, and
{name1} falls to the ground with a loud shout. Taking your gun you're aiming
the bus and starting to shoot at it as fast as you can. Sniper disappears
in the dark car inners, so {name2} takes down {hisher2} gun, lifting
{name1} and pulling {himher1} to the Train under your cover fire.
{name1} getting -35 health
{name2} getting -20 energy""",
                        "effects": {
                            "char_1": {"health": -35},
                            "char_2": {"energy": -20},
                        },
                    },
                    {
                        "score": range(20, 40),
                        "desc": """By your order {name1} and {name2} taking their gears and walking
to the bus. Looking at the car through binoculars you catch some kind
of a movement there. You whistles to notice your people about probable
troubles, and they taking lower poses. In the next second bus starts to
sway, and gun flames are blinking in the car's windows. {name1} and {name2}
shooting back at the same moment, but gang in the vehicle seems to be
more numerous, so they both retreating to the Train. Enemy gun fire
is terribly inaccurate, still, bullets are flying and flying to you,
throwing sparkles all around and ringing with the Train metal. You're
commanding to start moving, and {name1} with {name2} are jumping on the
Train on the run. Rival bullets following you for two more minutes,
and then suddenly falls silent. Train getting -40 damnability""",
                        "effects": {"train": {"damnability": -40}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """{name1} and {name2} taking their guns and moving in the direction
of the bus. Nearlands of the vehicle seems silent, so your people are
moving to the spot fast, but in some moment both are suddenly stopping.
You're passing your gaze around to understand what has gone wrong.
Jeep! Big black jeep roaring in a distance of kilometer seems to be
heading to the old bus! Feeling the bad luck you're shouting to your
people: "{name1}, {name2}, get back!". Gazing at each other for a second
they are turning around and retreating to the Train. Jeep in the same
time approaches the bus, several armed people are jumping outside.
Their mood seems to be aggressive, still, they doesn't start firing.
It's better to move along before they changed their mind.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """Driven by your command, {name1} and {name2} are taking the
direction to the old vehicle. As the meadow looks too open, they are
running fast to cross it as soon as possible. Disappearing within the
car your people a starting to rummage through it, swinging the old metal
carcass. While it all happening you're seeing a big jeep on a horizon.
Whistling loudly to your people you're preparing for a fight. It takes
two more minutes for {name1} and {name2} to jump outside the bus. The
gang in the jeep, approaching fast, are starting to shoot, and you're
opening fire back. {name1} and {name2}, using your cover shooting, are
returning back to the Train with several banknotes, and you're
deciding to move along before the bus beholders came too close.
You're getting +60$""",
                        "effects": {"money": 60},
                    },
                    {
                        "score": range(80, 100),
                        "desc": """While you were deciding who to send for a search, several
skinhead scums are jumped out of the bus. Your whole team seeing
them starts to shoot, and after six-eight seconds all of the rivals are
falling down on the ground. Taking a quick look at the vehicle through
binoculars you're commanding {name1} and {name2} to go to it. They
both energetically jumping off the Train and moving to the bus. You're
staying on the watch for case if more skinheads will come. Your
people entering inside the car, and returning back into a field of
view in less than thirty seconds. Getting back to the Train, they
showing you a bunch of crumpled dollars.
You're getting +100$""",
                        "effects": {"money": 100},
                    },
                ),
            },
            {  # 4
                "name": "Gas Station",
                "type": "Enemy Camp",
                "class_weights": {"soldier": 22.5, "raider": 7, "anarchist": 17},
                "assignees": 2,
                "day_part_weights": {
                    "night": 4,
                    "morning": 5,
                    "noon": 10,
                    "evening": 2,
                },
                "desc": """For at least twenty minutes you've been watching a highway to the left
of the railway. No cars, no light posts - road was completely empty.
But, finally, you're seeing a white square advertisement sign of a
small gas station. There is no vehicle nearby, nor people, otherwise
the building looks well maintained. Hm-m. Fuel - is always good, but
suspicious silence of the nearlands makes you little bit wary.
Place should be checked for resources, and if to send someone, you
should send two, so that messengers could deal with possible
troubles together.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """{name1} and {name2} are closing to the gas station, seeing a lot
of bullet shells scattered all around. They throw gazes at each other
and proceeding further much more slower. Entering into the looted
building, full of broken metal, plastic and wood stuff, they decide
to turn around and move back to the Train, but in that moment gun
shot thunders in the air, and the gas automates exploding with
horrorable noize. {name2} gets back to the reality first, and sees
that {name1} has a lot of cut wounds. Taking a quick look around,
{heshe2} detects no threats - seems, the one tried to explode them,
and retreated right after the shot. Lifting {name1} on the shoulders,
{heshe2} moves back to the Train.
{name1} getting -45 health
{name2} getting -10 health""",
                        "effects": {
                            "char_1": {"health": -45},
                            "char_2": {"health": -10},
                        },
                    },
                    {
                        "score": range(20, 40),
                        "desc": """{name1} and {name2} starting to move to the gas station by your
command. It takes a couple of minutes for them to come to the
building, which looks like people were here seconds ago. Entering
inside, {name1} and {name2} trying to find something really useful,
but only see bubble gum, chips and crackers. Suddenly, {name1} catches
{hisher1} attention on a strong smoke smell. Throwing a look through
the window, {heshe1} pushes {name2} and jerkely runs to the entrance.
{name2} follows {himher1}, and outside they see that someone surrounded
them with a ring of fire. "Faster!" - {name2} commands and runs
through the wall of flame, trying to cross it before it grown too strong.
Breaking through the fire, they see no one, no ambush or something.
Strange. With a couple of scorches they return to the Train.
{name1} and {name2} getting -10 health""",
                        "effects": {
                            "char_1": {"health": -10},
                            "char_2": {"health": -10},
                        },
                    },
                    {
                        "score": range(40, 60),
                        "desc": """You're choosing {name1} and {name2} as messengers for this walk.
They grab their stuff and take the direction to the gas station. Getting
closer to the building, they hear music. More than that, entering the
station they see several people: cashier, security guard guy and waiter.
Not to scare anyone they move their guns down, and doing a try
to talk with the gas station inhabitants, but all of them are speaking
at some weird language, which {name1} and {name2} doesn't know. As
dwellers doesn't seem to be dangerous, just several people, who still
lives here despite the End of Days, {name1} and {name2} deciding
to leave them as they were and move along.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """{name1} and {name2} moving to the gas station by your order.
Getting closer to the building they hear music, and see three people
within. In the next moment from the other side of the station four
skinheads with guns are appearing, with clear intent to attack the
gas point. {name1} and {name2}, not yet detected by robbers, upper their
guns and shooting off all of these cruds. The station dwellers moving
outside the building to see what's happening, and understand that your
people saved them from skinheads. They applaud {name1} and {name2}
speaking of weird language unfamiliar to your messengers. {name1} and
{name2} nod their heads, turning back to the Train, but one of the
dwellers stops them and gives them several dollar banknotes.
You're getting +70$""",
                        "effects": {"money": 70},
                    },
                    {
                        "score": range(80, 100),
                        "desc": """{name1} and {name2} fastly moving to the gas station. Getting
closer, they slow down, but after several seconds they see that the
building is abandoned. The glass door is open, music is still playing,
but dust lies everywhere and silence. {name1} and {name2} together
walking around the station, enter it and, seeing no threats, splitting
to take two things simultaneously: cash and fuel. Cash machine,
fortunately, is open, and {name2} finds a canister very fast. Filling
it to the brim, {name1} and {name2} in a good mood returning back
to the Train with their catch.
You're getting +90$ and fuel for 50 miles""",
                        "effects": {"money": 90},
                    },
                ),
            },
            {  # 5
                "name": "Trailers",
                "type": "Enemy Camp",
                "class_weights": {"soldier": 15, "raider": 4, "anarchist": 11},
                "assignees": 3,
                "day_part_weights": {
                    "night": 10,
                    "morning": 0,
                    "noon": 4,
                    "evening": 7,
                },
                "desc": """From a very long distance you're catching your eyes on several grey
rectangles. Buses? That can promise troubles as well as a good place
for looting. While the Train getting closer to the vehicle, it becomes
clearer that it's not just a bunch of cars, it's a small auto camp.
Five big trailers with clotheslines stretched between them, soccer
balls and bonfires looking quiet, but definitely inhabited. You're
not able to find any human by your eyes, and that fact makes the
situation even harder: there can be dozens of fighters there. It
makes sense to prepare well before entering this trailer camp.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You're making a decision to send {name1}, {name2} and
{name3} to investigate the trailer camp. They're taking their gear and
move towards the grey cars. Nothing promises troubles for several
minutes, but at some moment car engines tearing the air apart. You
all uppering your guns to fight back the enemy. Trailers are starting
to skid, throwing grey dust all around, and your messengers making
few steps back to the Train side not to get lost in these clouds. Red
and white trailers lights are floating in the grey shroud, but you're
hearing no shots. They are just leaving. Taking few more seconds to
think, you're commanding your people to return back to the crew.""",
                        "effects": {},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """You're deciding to send {name1}, {name2} and {name3} for a recon
of the place. While they are gearing up, you're looking at the trailers
camp trying to understand, if there is an ambush there. Once you hear
the vehicle engines starting, and in the next second trailers are
getting under way. Your people standing up just beside you, managing
to find out what is going on. "Looks like they are leaving." - {name2}
says. "Well, at least they didn't start to shoot." - {name1} adds. Yes,
that's definitely a good thing... Trailers are distancing fast, and the
dust settles to the ground, unveiling some stuff left by those people.
"Let's take a look at it!" - {name2} pronounces and jumps off the Train.
You're finding a cure that can heal 15 health of one character""",
                        "effects": {"select_char": {"health": 15}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """{name1}, {name2} and {name3} jumping off the Train to do a recon
of the trailer camp. In the same moment grey cars are starting their
engines and making a spurt to leave the place. Your people are holding
several seconds pause to see what will happen next... All the trailers
except one are moving away fast. {name3} throws a gaze to {name1} and
{name2} and points to the car with {hisher3} head. Closing to the vehicle,
they open it, and {name1} with {name3} are entering inside. It takes some
time for them to search through the car. It doesn't give a lot of
lucky finds, mostly there is just an old useless stuff, like someone very
old and most likely little bit mad was living in the truck, but at least
{name3} finds 30$ in there. With this find your messengers return back.
You're getting 30$""",
                        "effects": {"money": 30},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """By your command, {name1}, {name2} and {name3} taking their gear
and jumping to the ground. Right in this second all the trailers, except
one, spurt away. In the remaining trailer your people hear some fuss.
While they are getting closer to the vehicle, the window of it opens,
and a gun barrel leans out, starting to shoot all around without aiming.
Making a circle movement around the trailer, your people open it and do
several shots inside. The rival gun silences. {name1} and {name2} enter
the car for several seconds and walk out together, holding a big tool
box. Lifting it onto the Train, {name2} puts {hisher2} hand in {hisher2} pocket and
gets out a bunch of dollar papers. "Plus to the filter" - {heshe2} smiles.
You're getting 1 smoke filter and 60$""",
                        "effects": {"money": 60, "smoke_filters": 1},
                    },
                    {
                        "score": range(80, 100),
                        "desc": """{name1}, {name2} and {name3} energetically jump off the Train
and take the direction to the trailers camp. After few seconds of
silence they hear some movement near the cars. Uppering their guns,
they see several skinheads with pistols, swingingly moving to them.
Not giving a chance, your people shoot out them and start to move
from one trailer to another. In every one of them they see injectors,
white powder, stinky vomit and one-three stoned to nearly death
skinheads. "A drug party, ha?" - {name2} says. - "Let's take what
is useful for us and leave them where they are." {name1} and {name3}
agreeing on that, and they three start to collect things.
You're getting 200$""",
                        "effects": {"money": 200},
                    },
                ),
            },
            {  # 6
                "name": "Construction",
                "type": "Enemy Camp",
                "class_weights": {"soldier": 15, "raider": 10, "anarchist": 5},
                "assignees": 3,
                "day_part_weights": {
                    "night": 0,
                    "morning": 2,
                    "noon": 6,
                    "evening": 10,
                },
                "desc": """Standing on a cool air, you're observing the horizon line. For the
few last hours you saw twelve wooden houses, burned to the ground.
Seems like someone is clearing these lands, probably skinheads. It's
worth staying sharp... Once you're seeing a two-floored construction.
Concrete, with metal rods, but definitely unfinished - there are no
doors, window glasses, roof, only bare walls. "Let's make a short stop
there!" - you're commanding. That's not very logical, but something
makes you think there is somewhat useful in this building. Still,
considering the burned houses nearby, it's better stay vigilant.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You're deciding to send {name1}, {name2} and {name3}
to recon the construction site. Your people are preparing for a walk,
but in the moment they are going to jump off the Train, you're hearing
some fuss at the building. Suddenly, a big guy with a machine gun appears
on the second floor, and flame of his gun starts to rush between two
concrete walls. Bullets loudly knocking on the Train sheathing, promising
a lot of damage. In some moment the guns silences, and you're uppering
your head. A lot of shot holes are gapping on the Train. Are these armor-
piercing bullets!? Is it worth getting this guy? It's probably better to
leave before this gun made even more damage to the locomotive.
The Train damnability -60""",
                        "effects": {"train": {"damnability": -60}},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """You're giving {name1}, {name2} and {name3} an order to check
the construction site. Taking their guns, your fighters are jumping off
the Train and getting to the place. The building seems to be completely
empty and uninhabited. There are no even signs of temporary camp. In
disappointed mood, {name2} catches {hisher2} eyes on the basement entrance.
"Oh, you think we should?" - {name1} asks, understanding where {name2}
gazes. Why not, your people are going down to the dark wet basement.
Flashlights are floating on an empty walls and floor. Nothing. "Do you
feel it?" - {name3} asks. - "Smells like canella". {name2} harshly
stops. "Canella?! We better go!". Starting to understand, your
messengers running out of the basement on to fresh air. "We should
lavage ourselves, it can be very poisonous." - {name3} finalizes.
{name1}, {name2} and {name3} getting -20 health""",
                        "effects": {"assignees": {"health": -20}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """You're sending {name1}, {name2} and {name3} to check the place.
While they are on their way, you're staying on a watch to prevent any
surprises. The Stench have taken near 10% of the Earth, but people already
became non compos. Or maybe they always were, the Stench only released
their atrocity, revealed it? While they were afraid of laws, they were
quiet, proving their true selves only inside. And now, when no one
knows what to do and what will happen next, when no one controls the
situations, when no one will come to help, they decided to do what
their nature whispers... You're seeing your people walking out of
the construction. Looking disappointed, {name2} from that far shows
that there was nothing useful there, nor interesting. Well, it's
time to start the engine.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """Your team mates - {name1}, {name2} and {name3} are taking a
direction to the construction site. Nothing promises troubles for some
time, but when they getting down to the basement, the cry tears air.
Fast uppering their guns, your messengers see a thin guy, holding
his hands above his head. "Don't touch me!" - he shouts. As he
doesn't have a weapon, {name1} takes {hisher1} gun aside. "He is
skinhead." - {heshe1} pronounces surely. "Yes, yes!" - the guy answers. -
"But they left me. Now I'm alone. Take my money and don't touch me!"
- he gets his left hand into the pocket and throws several banknotes
outside of it. "Don't touch me!". Raising the money, {name2} takes away
{hisher2} gun as well and points others to the exit.
You're getting 80$""",
                        "effects": {"money": 80},
                    },
                    {
                        "score": range(80, 100),
                        "desc": """{name1}, {name2} and {name3} jump off the Train and
run to the construction site. Getting closer, they smell smoke, so,
holding teamwise, they starting to move fast from one room to another,
covering each other and taking every turn on a sight. Skinheads,
confused and, probably, stoned, are appearing from time to time,
but your messengers are shooting them one by one without any delays.
Cleared the whole two-floored building in four minutes, they
make a short pause, and then start to rummage through rival
stuff. It doesn't look like a lot of useful things, but these
guys definitely had some money.
You're getting 130$""",
                        "effects": {"money": 130},
                    },
                ),
            },
            {  # 7
                "name": "Cloth Piece",
                "type": "Enemy Camp",
                "class_weights": {"soldier": 22.5, "raider": 14, "anarchist": 5},
                "assignees": 2,
                "day_part_weights": {
                    "night": 0,
                    "morning": 5,
                    "noon": 10,
                    "evening": 7,
                },
                "desc": """The horizon line is lost behind trees for hours. The lands seems
to be very wild, still, you've given an order to everyone to keep eyes
open. And in voluntary minute you're hearing your teammates calling you
outside the cabin. Exiting the Train deckhouse, you're taking a binocular
and gazing into the pointed direction. First you don't see anything
except trees. But after few seconds a big piece of dark green cloth
reveals, strained between two tree trunks. "Looks like a shelter" - you're
pronouncing, thinking how many people should be sent there.
Probably, two fighters will be enough.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """After overthinking the situation you're deciding to send
{name1} and {name2} for a scouting. They both take their gear and
jump off the Train. You see them moving to behind of the cloth piece...
Ten minutes passed, and finally you see your people running back to
the Train. While they are getting closer, you're starting to suspect
something wrong - too nervous is their behavior. "There was an ambush."
- {name2} says, climbing to the Train. - "They've taken {name1} as a
hostage and demanded ransom." {name1} climbs to the Train next:
"Sorry!". {name2} continues: "I've gave them 90$ to free {himher1}.
Let's go before they wanted more."
You losing 90$""",
                        "effects": {"money": -90},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """You're sending {name1} and {name2} to see what is this
piece of cloth is for. Your people run to the place fast, but in last
thirty meters they slow down and start to move much more careful. The
strained cloth seems to be a disguise - they find metal dishes, backpacks
and some other stuff behind it. The camp is long forsaken, still, as
they are already there, your messengers rummaging the things. In
some moment a loud rustle sounds in air, and big web with stones
falls down to {name1}'s head. {name2}, who was standing few meters
aside, raises the gun and circles on {hisher2} place... But no one
showing up... {name1} in that time gets out of the web and, covering
a blooding wound on {hisher1} head, touches {name2} to show that
{heshe1}'s ready to return back to the Train. And they return fast.
{name1} getting -20 health""",
                        "effects": {"char_1": {"health": -20}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """After a couple of minutes of thinking you're deciding to
send {name1} and {name2} to check the place. They fastly running to the
strained cloth and hiding behind it; silence and still falls on the near
lands. While waiting them, the Stench comes on your mind. Are there
people who can survive in it? Is there a kind of natural immunity to
this phenomenon? You never heard about such a thing. Though, news in
our days are not very often at all. Only death statistics and territory
cover reports... Finally, you see your people returning back. There
is nothing in their hands, so you doesn't wonder, when {name1} comes
closer and says: "Negative!". Well, time to continue the path.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """You're sending {name1} and {name2} for a short
recon of the place. In fast pace they run to the cloth piece, and
when the distance to it becomes less than twenty meters, several
skinheads jumping out of the strained cloth. Not giving any chances,
{name1} and {name2} with accurate shots dropping rivals one by one.
Ensuring there are no more threats, they start to search through the
wooden boxes, piled up behind the cloth. Most of them are already
empty, but {name1} and {name2} find a bunch of personal first aid
kits. Giving high five to each other, they take the catch and,
satisfied, returning back to the team.
Your teammates getting +10 health""",
                        "effects": {"all": {"health": 10}},
                    },
                    {
                        "score": range(80, 100),
                        "desc": """After little overthinking you're decided to send
{name1} and {name2} to take a look at the place. Fastly moving to
the spot, they hide behing the strained cloth, and after few seconds
show up again with a big metal ammo box. Seeing this, you're jumping
off the Train and moving towards them to cover, as their hands are
busy. When you're getting closer, {name1} explains: "No one at home!
We decided to take that stuff, as there is a couple of gnawed bodies
in the camp. Doesn't look like a good campers." Uppering the heavy
ammo box on to the Train together, you're giving an order to start the
engine. With this catch you'll save some money on the next stop.
You're getting 170$""",
                        "effects": {"money": 170},
                    },
                ),
            },
        ),
        "looting": (
            {  # 1
                "name": "Abandoned Car",
                "type": "Looting",
                "class_weights": {"soldier": 22.5, "raider": 45, "anarchist": 9},
                "assignees": 1,
                "day_part_weights": {
                    "night": 0,
                    "morning": 3,
                    "noon": 10,
                    "evening": 5,
                },
                "desc": """At the first look you didn't pay attention to
a dark green spot in the middle of the meadow. But in the next
second it becomes clear that it is not a part of the landscape,
it's a car! It looks abandoned and old, standing there for a
long time. Still, glass seems to be unbroken, and doors closed,
so it may make sense to check if something remain within.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """As the car stands in 50 meters far from
railway, you're sending {name1} alone to search it for supplies.
{name1} approaches to the car thinking: where to look first?
Glove compartment! Of course, {heshe1}'s opening the door, taking
a sit, and starts to feel the contain of the glove compartment.
"It's too hot in this car." - {name1} thinking, but in the next
moment {heshe1} feels something crawls on {hisher1} legs.
Turning {hisher1} look down {heshe1} sees hundreds of big red
ants creeping on {hisher1} knees and chest. Trying to drop them off,
{heshe1} only makes them crawl on hands. With screems {heshe1}
jumps out of the car and starts to roll on the grass trying
to deal with agressive insects.
{name1} getting -50 energy and -15 health.""",
                        "effects": {"char_1": {"energy": -50, "health": -15}},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """As the car stands not very far from
railway, you're sending {name1} alone to search it for supplies.
{name1} energetically moves to the car and starts a find. The
car looks old, and feels hot inside, but seems like no one looted it
yet. Still, vehicle insides doesn't contain anything interesting. {name1}
gets out and makes a circle around the car. Trunk - here is the place
to search! Opening the trunk {heshe1} sees a shovel and a big sack.
Fermer staff? Taking out {hisher1} knife, {heshe1} flogs the sack. The
first thing that falls from it is a human skull with two small holes
on the occiput. Looks like someone just tried to cover his tracks...
{name1} getting -15 energy.""",
                        "effects": {"char_1": {"energy": -15}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """As the car stands close to a railway, you've
sent {name1} alone to look for supplies in the vehicle. {name1}
moves to the car, opens it and gets inside. It's hot and dusty within
the car, every movement raises the dense fug, but {hisher1} search
doesn't end with nothing. It appeared that a first aid kit is still there,
and opening it {name1} sees that it contains several not overdue meds!
That can help to regain 10 points of health of a single character.""",
                        "effects": {"select_char": {"health": 10}},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """The car stands close enough to a railway to fear
nothing, so you're sending {name1} alone for a looting. {name1} runs
to the car, and disappears inside. From the train you're not able to
see what's {heshe1} doing there, and it takes a half of hour to wait for
the results. {name1} jumps out of the car and moves to you with a small
box in {hisher1} hands. "That guy wasn't very thrifty, I've found only
these tools." - {heshe1} says. Well, it's still better than nothing:
we can repair the train a little.
Train damnability +100.""",
                        "effects": {"train": {"damnability": 100}},
                    },
                    {
                        "score": range(80, 101),
                        "desc": """The car stand too close to the railway to fear
anything, so you're sending {name1} alone for a search. {name1} closes
to the car fast and starts to sort through it, throwing away useless stuff,
like toys, tent, rubber boat... You're looking at all of these from the train
starting to think this stop is pointless. But then {name1} moves to the
trunk, opens it and screams victoriously. In the next second you see a big
grey tool box in {hisher1} hands, and uppering your hand with a like-finger.
You're getting a smoke filter in a good shape.""",
                        "effects": {"smoke_filters": 1},
                    },
                ),
            },
            {  # 2
                "name": "Meadow Tent",
                "type": "Looting",
                "class_weights": {"soldier": 6, "raider": 22.5, "anarchist": 16},
                "assignees": 2,
                "day_part_weights": {
                    "night": 0,
                    "morning": 7,
                    "noon": 10,
                    "evening": 3,
                },
                "desc": """The big dark green spot on the meadow attracted your
attention in the same moment. What do we have here? Seems to be an
abandoned tent. There are no any signs of a bonfire, smoke, or any
human, so the camp is probably long forsaken. Still something useful
can remain there, who knows. It's worth checking. The place seems to be
open, quite and calm, but it's little bit distant. If something will
go wrong it'll be a long way back for your teammates. So a couple
of people should be sent for a surprise case.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You're sending {name1} and {name2} as a loot party.
Closing to the place they see several backpacks lying around
the tent. "I'll check the tent" - {name1} says and moves towards
it. {name2} takes {hisher2} hands on backpacks. One by one {heshe2}
opens them and sees ropes, climber equipment, fishing stuff, but there
is definitely no anything we can use. Suddenly {heshe2} hears {name1}
shouting from the tent. {name2} takes {hisher2} gun and jumps to the
teammate. "Snake! A God damn snake!" - {heshe1} shouts and shows a bloody
hand. With a short gaze {name2} sees that there is no supplies in the
tent, so {heshe2} takes {name1} and pulls {himher1} back to Train.
{name1} getting -50 energy and -30 health
{name2} getting -20 energy""",
                        "effects": {
                            "char_1": {"energy": -50, "health": -30},
                            "char_2": {"energy": -20},
                        },
                    },
                    {
                        "score": range(20, 40),
                        "desc": """{name1} and {name2} are moving to the tent by your
command. The vibrations of the train still tremble at their feet, but the
still ground feels good. Air smells with grass and flowers, and warm
soft wind complements the place. But in the next moment {name1} feels
something else. Rotten meat. {name2} glances at {himher1} as {heshe2}
smells the same. Closing to the tent they are starting to understand
what is the source of that stink. {name2} moves forward. "Let me do
this!" - {heshe2} pulls the zipper, and directs a lantern into the tent. Bodies!
Two rotten bodies, with bones sticking out, maggots, and nothing more.
Both characters are getting -30 energy.""",
                        "effects": {
                            "char_1": {"energy": -30},
                            "char_2": {"energy": -30},
                        },
                    },
                    {
                        "score": range(40, 60),
                        "desc": """You've decided to send {name1} and {name2} to check the place.
They are taking their guns and moving to the tent, while you're looking
for possible threats. The meadow seems to be still and quiet though.
Your people are closing to the tent and starting to walk around it and
prowl. It appears there are several backpacks at the forsaken camp place,
but {name1} and {name2} doesn't take anything with them. Nothing
interesting? You're waiting for several more minutes, but nothing
changes. Finally, {name1} and {name2} are opening the tent, taking a
quick look inside, and turning back to the Train. Obviously, there
was nothing useful in there. At all.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """{name1} and {name2} are taking their things and moving to the
camp place. The meadow looks still, smells with grass and flowers,
warm wind makes the way pleasant. Closing to the tent {name1} and
{name2} are starting to search for supplies through the things left
in the camp. Ropes, empty cans, some climber stuff, even an album with
old photos. Finding nothing {name1} decides to take a look at the tent
- {heshe1} pulls the zipper and stick {hisher1} head into the stifling inners.
The tent looks empty at the first gaze, but suddenly {name1} caughts
{hisher1} eyes on a bottle of an energy drink. "Well, it's something!"
 - {heshe1} pronounces and takes the bottle.
Single character can get +40 energy""",
                        "effects": {"select_char": {"energy": 40}},
                    },
                    {
                        "score": range(80, 101),
                        "desc": """You're sending {name1} and {name2} to search the camp for
anything useful. Your people are getting to the forsaken tent in two
minutes and starting a find. You're seeing them rummaging in bags left
there, but nothing gives a sign of lucky find. Done with backpacks
{name2} opens the tent zipper and moves inside. It takes a few minutes
for {himher2} to deal with the inner stuff, but to everyone's joy
{heshe2} shows up with a white aid kit. Smiling both {name1} and {name2}
are returning to Train with this burden.
You're getting 1 medicine box.""",
                        "effects": {"medicine_boxes": 1},
                    },
                ),
            },
            {  # 3
                "name": "Old Hut",
                "type": "Looting",
                "class_weights": {"soldier": 10, "raider": 15, "anarchist": 3},
                "assignees": 3,
                "day_part_weights": {
                    "night": 8,
                    "morning": 2,
                    "noon": 5,
                    "evening": 10,
                },
                "desc": """Called by one of your teammates, you're walking out of
the cabin and in the same moment seeing an old hut not far from the
railway. Putting binoculars to your eyes you're looking at it with good
feeling. The house seems to be very old, built with dark ancient
logs. No smoke rises from the chimney. Taking a few second to assess
the prospects, you're thinking about sending three people to search
the place for anything that can help you on the road. And, who knows,
maybe someone is still living in that ancient hut...""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You're commanding {name1}, {name2} and {name3}
to gear up. People are taking their stuff and moving to the hut.
Approaching to it they see that the house is long abandoned, but they
moving into it for a lookup anyway. They splitting up: one person for
one room. Finding nothing, but dust, within half of hour, almost without
hope they open a floor basement entrance, and hooray! They see
several tens of cans! With such a catch, you decided to throw a feast!
But after several hours it comes clear that food expired.
All of your teammates are getting -40 energy""",
                        "effects": {"all": {"energy": -40}},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """{name1}, {name2} and {name3} are gearing up for
a walk. It takes few minutes for them to reach the hut. They see an
opened door, broken windows and wild weeds right before the entrance -
looks like this place is long forsaken. "Well, we're already here,
let's take a look!" - {name2} proposes. People are entering the house,
and in the next moment {name2}, who went upfront, falls on the ground
under a dog attack. {name1} and {name3} are raising their guns, but
they can't shoot, as it's a big risk to shot {name2} instead of the
big brute. Removing weapons they are getting to {himher2} to fight
the animal with their hands.
{name2} getting -20 health and -40 energy
{name1} and {name3} getting -25 energy""",
                        "effects": {
                            "char_2": {"energy": -40, "health": -20},
                            "char_1": {"energy": -25},
                            "char_3": {"energy": -25},
                        },
                    },
                    {
                        "score": range(40, 60),
                        "desc": """You're sending {name1}, {name2} and {name3} for a search.
People are easy running to the hut and disappearing in it. You're
looking for them from Train. Time passing, but nothing happens, so
you're starting to get nervous. Suddenly, you hear cries and two shots.
That doesn't sound good! Two minutes passes, and finally you're seeing
your people. They are moving fast to the Train, keeping their backside
on sights. But no one follows them. Coming closer {name1} explains to
you what happened back there: "Big dog, looks like it lives there.
And we found nothing". Your people are getting on the Train in
disappointed mood, and you're commanding to move.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """{name1}, {name2} and {name3} are gearing up and taking
direction to the hut. Approaching to it they see that wood building is long
abandoned: weeds are crossing the door, windows are broken, and
stillness fills the air. {name2} and {name3} are moving into the house, while
{name1} is standing outside on a watch. It takes a lot of time for {name3}
to check all the broken furniture in the first room, but {heshe3} finds
nothing. {name2} appears to become more lucky: {heshe2} managed to
find 30$ within a lady's old bag. With such a results {name2} and
{name3} are leaving the silent and dusty house, and joining {name1}
to get back to Train and others.""",
                        "effects": {"money": 30},
                    },
                    {
                        "score": range(80, 101),
                        "desc": """You're asking {name1}, {name2} and {name3} to go for a
search. They're taking their things and fastly moving to the hut.
Splitting up - one person to one room - they are rummaging through old
broken furniture, clothes that is covering the floor with a thick layer
of dust, metal dishes and other stuff. Nothing useful comes to your
messengers for some time. "Oh, I got something!" - {name2} shouts loudly.
{name1} and {name3} moving to the room {heshe2} was checking, and seeing a
big tool kit. {name1} and {name2} are taking it together and moving
back to Train, while {name3} is watching around for possible threats.
Train damnability +90""",
                        "effects": {"train": {"damnability": 90}},
                    },
                ),
            },
            {  # 4
                "name": "Monastery",
                "type": "Looting",
                "class_weights": {"soldier": 9, "raider": 15, "anarchist": 4},
                "assignees": 3,
                "day_part_weights": {
                    "night": 10,
                    "morning": 2,
                    "noon": 5,
                    "evening": 8,
                },
                "desc": """You've caught your eyes on some kind of big dark spike
from a very long distance. It was difficult to understand what it
actually is, but when the Train went around a hill, and the building
appeared before you in its best, you're seeing an old monastery. Its
black wood looks rotten, and the big hole on roof makes it clear that
this building was left years ago. Still the monastery in such a
wilderness place should have had a big supplies storage. Monks
probably didn't take everything when they were leaving.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You're sending {name1}, {name2} and {name3} to
the monastery. {name1} and {name3} are entering the old building,
while {name2} stays outside to cover team mates retreat in case of
problems. For some time {heshe2} doesn't hear anything, so {heshe2}
relaxes a little. But in the next minute eerie noise comes from
the monastery. Taking a look inside {name2} sees that part of the
roof collapsed! Jumping inside {heshe2} start to call for {name1}
and {name3}: fortunately both are alive, though it takes some
time to dig them out of the wreck.
{name1} and {name3} getting -30 health
{name2} getting -30 energy""",
                        "effects": {
                            "char_1": {"health": -30},
                            "char_2": {"energy": -30},
                            "char_3": {"health": -30},
                        },
                    },
                    {
                        "score": range(20, 40),
                        "desc": """{name1}, {name2} and {name3} are moving to the
monastery. Entering it they see dust, web and a lot of wood wreck.
Looks like this building is looted long ago. Still {name1}, {name2}
and {name3} are splitting to search through the place faster.
Everything goes okay, until {name2} and {name3} hear an awful noise
and {name1} cry. They run to the sounds source, and find {name1}
felt through the old wood floor. Putting the guns down they are
getting to the hole to lift {himher1} from it. Its luck that {heshe1}
didn't get any injury, only a couple of big scratches.
{name1} getting -10 health and -15 energy
{name2} and {name3} getting -10 energy""",
                        "effects": {
                            "char_1": {"energy": -15, "health": -10},
                            "char_2": {"energy": -10},
                            "char_3": {"energy": -10},
                        },
                    },
                    {
                        "score": range(40, 60),
                        "desc": """You're letting {name1}, {name2} and {name3} to go for a find.
They are closing to the monastery fast, but in some moment hear
strange sounds and shouts. Moving closer to the building, they decide
to take a look through the window. {name2} sets a knee to give a lift
to {name3}, while {name1} stands near on a watch for troubles, as in
this noise they hear human voices, and they are many. Lifting up {name3},
takes a look inside the monastery, and sees at least forty people
in there. Dirty, unkempt and completely crazy, they are ripping to shreds
several animals and eating them raw, all covered in blood. Seems like kind
of cultists are celebrating the End of the World. {name3} moves down and
silently explains what {heshe3} saw. Deciding not to disturb this mad
gathering, your people returning back to the Train.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """On your command {name1}, {name2} and {name3} are moving
to the monastery. First they are approaching the building quietly, but
soon they see it's completely forsaken long time ago. Entering inside
they find a lot of wood wreck. Air smells mold and dust, strong silence
soar in the old monastery. Walking along the building your people
discover a huge wall icon, which seems untouched by time. Colors are
saturated, lack of any cracks or dirt - it looks surprisingly well
for this place. {name1}, {name2} and {name3} spending a couple of
minutes staring at the art object, and its beauty in the midst of
the old monastery devastation inspires them to survive anything.
{name1}, {name2} and {name3} getting +20 health""",
                        "effects": {"assignees": {"health": 20}},
                    },
                    {
                        "score": range(80, 101),
                        "desc": """By your command {name1}, {name2} and {name3} going to the
monastery. Entering the old building they see a lot of wood and metal
wreck. Nothing valuable though, so they are splitting for a more
careful search. {name3} chooses the basement and goes down into it.
Walls looking wet, spider web is everywhere, but {heshe3} sees a big chest
in the first second. The rusty lock doesn't want to broke, so {name3}
calls others. {name1} and {name2} are coming into the basement and with
strength of the three they manage to open the chest. What's the pleasure
when they see gold dishes in it! These can be sold for a good money!
You're getting +40$""",
                        "effects": {"money": 40},
                    },
                ),
            },
            {  # 5
                "name": "Wrecked Truck",
                "type": "Looting",
                "class_weights": {"soldier": 7, "raider": 22.5, "anarchist": 16},
                "assignees": 2,
                "day_part_weights": {
                    "night": 2,
                    "morning": 4,
                    "noon": 10,
                    "evening": 8,
                },
                "desc": """You're looking at the horizon line trying to find a sign of a
civilization. A couple of hours passed, and there were no single building,
litter or any other sign of human. What are these wild plains? But once
a distant grey spot attracts your eyes. You're taking a look at it through
your binocular. Truck! Even from that big distance you can say it is
damaged bad: at least one wheel is ripped off and the metal cargo hold
is dented. Still, you can afford a short stop and fast recon of the
transport crash site. It's not accurate to say from that distance, but
looks like there are a lot of things scattered around it.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """{name1} and {name2} are going to the distant truck in
hope to find something valuable there. It takes at least a half of hour
for them to get to the transport. Looking through a binocular you see
them walking around the car, squatting, touching some stuff lying
all around the truck... Time passes and passes, but you don't detect
any signs of a lucky find. Spending few more minutes there {name1}
and {name2} are returning back to the Train. "Someone outstripped
us." - {name2} explains. - "And didn't left a tiny bit of the cargo." """,
                        "effects": {},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """You're commanding {name1} and {name2} to go to the
truck and do a search through its last resting place. They are running to
the spot energetically and starting to rummage in the broken plastic boxes
lying near the car. Most part of them are already emptied by someone
else, but {name1} and {name2} not losing hope. And after rummaging not
less than twenty containers they finally see one untouched. Opening it
they are staring at a bunch of metal details. And tools! "With this stuff
we can repair our Train a little!" - {name2} whopping. They are taking
the box together and returning back to you with it.
Train damnability +40""",
                        "effects": {"train": {"damnability": 90}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """You're sending {name1} with {name2} to take a look
at the crash site. {name2} takes a fuel tank in hope there will be
something to bring back. Both they are moving to the damaged truck
and starting to search through the plastic boxes scatter around the
place. At the first minute they understand that someone already emptied
every container at the place, probably, the same one who attacked the
truck - they see a lot of sleeves and shot holes. Taking a look
inside the car cabin {name2} finds that it also emptied. Almost without
hope {heshe2} moves to the gas tank, and... Yes! There is petrol! Inhaling
its strong smell {name2} drains the gasoline, and, satisfied, your people
are returning back to the Train.
You're getting diesel fuel for 50 more miles.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """{name1} and {name2} are taking their guns and going
to the damaged truck. Fastly closing to it they see a lot of sleeves and
shot holes - it's not just a crash, someone attacked the transport! There
are no bodies around, but your people notice several big and dark blood
spots. They are exchanging their glances and starting to open plastic
containers left right on the road one by one. Mostly they are empty, but
in one of them {name1} finds a couple of aid kits. The first one seems
damaged bad, but the second looks okay, so {name1} grabs it. As {name2}
didn't find anything, but broken containers, your people returning
back to the Train with this only find.
You're getting +1 medicine box""",
                        "effects": {"medicine_boxes": 1},
                    },
                    {
                        "score": range(80, 101),
                        "desc": """By your command {name1} and {name2} are gearing up and
taking a walk to the truck. Coming closer to it they see that a big fight
was here. Looks like a gang attacked the transport to rob it or something
like that. {name1} and {name2} starting to rummage through the boxes
scattered all around. The fight site appears to be looted several times
by different people, hopes to find something useful are fading with every
second, but suddenly {name2} sees an untouched container with energy
drinks. "Hey, {name1}, come here!" - {heshe2} shouts They are taking
the box together to bring it back to the Train.
Every character getting +35 energy""",
                        "effects": {"all": {"energy": 35}},
                    },
                ),
            },
            {  # 6
                "name": "Grey Smoke",
                "type": "Looting",
                "class_weights": {"soldier": 4, "raider": 15, "anarchist": 12},
                "assignees": 3,
                "day_part_weights": {
                    "night": 5,
                    "morning": 7,
                    "noon": 10,
                    "evening": 2,
                },
                "desc": """From a very long distance you are seeing a big, wide
straight column of thick grey smoke, rising from the forest in a
couple of kilometers from the railway. That seems questionably.
It can be either a big bonfire in a large human camp, or a forest
conflagration. In both cases the situation can turn very dangerous
for your messengers, so it makes sense to send several tough
fighters to see what's going on there.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You're sending {name1}, {name2} and {name3} for a recon,
admonishing them to be careful and cautious. Your people taking
a direction to the wide smoke column. It takes fifteen minutes for
them to come to the place, where they see a lot of fire sources. That's
definitely a forest conflagration! Not thinking too long, your people
turning around and moving back to the Train. The dense smoke doesn't
give an opportunity to navigate the way, so your messengers are
moving astray along the forest, consumed by flames, trying to find
the right direction for not less than half of hour. Finally, they
see the Train main lighter you're turned on to help them to get out.
Covered with soot and small scorches, inhaled smoke they are
getting back on the machine.
{name1}, {name2} and {name3} getting -20 health""",
                        "effects": {"assignees": {"health": -20}},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """Your recon party is moving to the pillar of grey smoke.
You're tracking their progress from the Train through binoculars. Your
people are running to the forest spot fast and disappear between dark
green trees. Thick grey smoke rises and rises, getting more wide with
every minute. No, it's not a bonfire, it's definitely a conflagration.
Time passes, and you're becoming nervous, as three of your team
mates are not showing up. Maybe it's worth to walk to the place by
yourself... Finally, you see them! Slow and tired, they return back
to the Train, inhaled a lot of smoke and probably intoxicated.
{name1}, {name2} and {name3} getting -25 energy.""",
                        "effects": {"assignees": {"energy": -25}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """{name1}, {name2} and {name3} are taking a direction to the smoke
column, by your command. Running fast, they come to the place in
twelve minutes and see a small wood hut, engulfed in flames. As there
are no screams or any movement, they could say there is no people
inside, at least, alive. The hut itself looks really ancient, it's most
likely was long forsaken. {name1}, rubbing his forehead, warmed up by
the fire, makes a step back: "Let's go until it's grown into the forest
conflagration, and locked us inside a ring of flames!". Without any
arguments {name2} and {name3} turning around and taking a direction
back to the Train.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """By your order, {name1}, {name2} and {name3} run to the grey
smoke column. Getting closer, they see a lot of red spots between the
trees - it's a forest conflagration, a big one! Throwing a gaze to others,
{name2} suddenly proposes: "Let's go hunting! Animals will run chaotically
away from flames and smoke, and food is something we always need."
Thinking a couple of seconds, {name1} and {name3} agree on that, and they
three are going to the forest... After twenty minutes of hunting they
getting a deer. Not very big, but it's even better - not a problem to get
it to the Train. "With this meat we can save some proviant money!" -
{name2} declares. - "Good job!"
You're getting +50$""",
                        "effects": {"money": 50},
                    },
                    {
                        "score": range(80, 101),
                        "desc": """Leaded by your order, {name1}, {name2} and {name3} moving
in the smoke column direction. Quickly getting to the place, they see a
big military truck, exploded with rocket launcher a couple of hours ago.
Blood, glass, metal and body parts of several soldiers are scattered all
around. Getting closer to the truck cargo hold, your people see big boxes
traces on the ground - somebody already looted the place. Still, {name3}
jumps onto the truck to take a closer look at the inner part of the
cargo hold. To everyone's joy, {heshe3} moves outside the car with a
big plastic box of tools. Seems like assaulters have only taken weapons.
Train damnability +70""",
                        "effects": {"train": {"damnability": 70}},
                    },
                ),
            },
            {  # 7
                "name": "Silo",
                "type": "Looting",
                "class_weights": {"soldier": 6, "raider": 22.5, "anarchist": 16},
                "assignees": 2,
                "day_part_weights": {
                    "night": 10,
                    "morning": 0,
                    "noon": 3,
                    "evening": 5,
                },
                "desc": """When the Train started to move along sown fields, you've concentrated
your gaze. Where fields, there are people and resources. And, yes,
in some moment you see a big brown silo. While the Train is getting
closer, you discerning a couple of small buildings near the metal
reservoir as well. From that distance they look quiet and deserted,
but they are definitely in a very good shape, so they are, probably,
populated. It's worth to send a couple of your people to check if
there is something useful for a road in there.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """{name1} and {name2} becomes your messengers this time.
They cross the silent wheat field without any sign of trouble, but,
getting closer to the buildings, both rising their weapons. {name1}
points to the small hut first, and they take the direction to it.
Suddenly, they hear some kind of a stomp, and in the next moment
giant bull pushes {name1} with his brown head, knocking {himher1}
down to the ground. {name2} lighting rapid turns around and shots
near the bull's legs, but the animal doesn't pay any attention and
prepares to kick {name1} again. Turning {hisher2} gun into its head,
{name2} kills the brute. In the next second {heshe2} sees two more
bulls moving out of the barn, and that is enough for {himher2} to help
{name1} get up and spurt back to the Train.
{name1} getting -35 health""",
                        "effects": {"char_1": {"health": -35}},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """{name1} and {name2}, chosen by you as a recon party,
are heading to the brown metal cylinder of the silo. Field and the
buildings looking quiet, only wooden creak sometime sounds in air.
Still, getting closer to the place, your people start to suspect something
wrong, as there are bullet holes on the walls, window glass, and smell of
death flyes in the air. Silently moving through the buildings, {name1}
and {name2} doesn't see anything useful, anything at all, like somebody
cleared the house without remainder. Deciding to take a look at the silo
itself, your people are getting to it and opening the metal door. All of
a sudden, black swarm of flies breaks out of the silo, and your
teammates see tens of dead bodies in there. "Let's go, before the author
came back!" - {name1} says, and they both fastly turning back.
{name1} and {name2} getting -15 energy""",
                        "effects": {"assignees": {"energy": -15}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """{name1} and {name2}, by your order, taking their gear
and moving to the silo. Nothing promises any troubles, but when your
people are getting closer to the buildings, four men with guns
showing up. They all look like hereditary rednecks, but their M16 and
Beretta's shines like it's a special forces property. "What do you
want? You doesn't look like skinheads." - an old man steps forward.
{name1} and {name2} exchange glances, but before they started to talk,
the man continues: "We don't wanna hurt anyone, but you better go away".
{name1} makes a step back: "No problem, we'll go". Not touching
locals, your people making a slow turn around and heading back to you.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """You're commanding {name1} and {name2} to go for a recon.
Your teammates are closing to the place, but four hulk rednecks with
guns appearing towards them. {name1} and {name2} stopping, trying to show
they are not going to attack. An old man makes a step forward: "Aren't
you folks, who came from abroad, and now killing skinheads all around?"
{name1} and {name2} exchange their gazes. "Sounds like us" - {name2} answers.
"Benny, give them some paper!" - old man shouts. Tall redneck makes
several long steps towards your people and holds out a 50$ banknote.
"Those bastards killed a lot of good folks around here." - the old man
pronounces loudly. - "Thanks for clearing this filth. Keep up the good
work!" - he uppers his hand, and all of the rednecks are turning back
to their place. In good mood your people returning to you.
You're getting +50$""",
                        "effects": {"money": 50},
                    },
                    {
                        "score": range(80, 101),
                        "desc": """You're sending {name1} and {name2} to take a closer look
at the place. Your messengers closing to the silo; silence meets them,
so they entering inside the buildings. The lack of any furniture
or sign of people - seems like the place was forsaken some time ago,
and hosts have taken everything with them. Walking outside the last
of three buildings, {name1} points to the metal cylinder of silo
with {hisher1} head. {name2} agrees on that, and they both getting
closer to it. Opening the steel door, they see that there is no
even a gram of grain. But pointing a flashlight inside the structure,
they catch their eyes on two metal boxes. {name2} jumps inside
and opens the first one: medicines! "Whoh!" - {heshe2} shouts and
opens the second one: a smoke filter! Now, that's a find!
You're getting 1 smoke filter and 1 medicine box""",
                        "effects": {"medicine_boxes": 1, "smoke_filters": 1},
                    },
                ),
            },
        ),
        "meet": (
            {  # 1
                "name": "Tents",
                "type": "Meet",
                "class_weights": {"soldier": 5, "anarchist": 22.5, "raider": 17},
                "assignees": 2,
                "day_part_weights": {
                    "night": 0,
                    "morning": 10,
                    "noon": 7,
                    "evening": 4,
                },
                "desc": """Gazing around, you're catching your eyes on a thick column of smoke
rising right from the ground. A look through binoculars unveils
that there is a tent camp at the bottom of the smoke pillar, and
you're giving your people an order to prepare for a fight. At the
next few seconds you understand that there are mostly women and
children in the camp. Looks strange - during our days it's not very
sensibly to travel without several protectors. Still, they may had
not be planning so, and it's worth checking these people out. Maybe
they need assistance or something. Two messengers should be enough.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You're ordering {name1} and {name2} to gently approach the
tent camp not to scare inhabitants, and see what's going on in
there. Your fighters walking to the place, and you see them talking
with dwellers. Suddenly, several men rise from the tents, and in the
next moment jump to {name1} and {name2}! You can't say from that
distance, but seems like those people don't have guns, only knives.
Doing several shots, {name1} and {name2} running back to the Train.
No one follows them - probably, all the attackers were killed. Jumping
on the Train, {name1} shows a big cut on {hisher1} shoulder. "Those
bastards want to join skinheads! Tried to kill us to impress them."
You nod to the machinist, ordering to start engine.
{name1} getting -10 health
{name2} getting Nervousness""",
                        "effects": {
                            "char_1": {"health": -10},
                            "char_2": {"add_trait": "Nervousness"},
                        },
                    },
                    {
                        "score": range(20, 40),
                        "desc": """{name1} and {name2} following your order to gently approach
the camp and see if everything is okay there. They move fast
for some time, but at some point they both stop. Straining your eyes,
you're trying to understand what's happening. Suddenly, several thugs
with knives and metal pipes rising from the tents, and run to your
people. Doing a bunch of shots, {name1} and {name2} turning back to
the Train. You hear a loud shout: "Killing will make you skinhead!" It's
clear! Uppering your gun, you're starting to cover your messengers with
fire. They successfully getting to the Train, and you all dropping rivals
with coordinated shooting. "Thanks!" - {name2} breaths. {name1} nods to
you. "Okay, let's move!" - you command, and the Train engine starts.
{name1} and {name2} getting -15 energy""",
                        "effects": {"assignees": {"energy": -15}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """You're sending {name1} and {name2} for a short recon. They
take their gear and move to the place. You're tracking them from
the Train, seeing how they carefully approach the camp; a couple of
women go to meet them. Their conversation lasts for several minutes,
and then {name1} and {name2} turning back to you. {name1} climb to
the locomotive first: "They are travelling to the nearest city. Not
fighters. We proposed them assistance, but they don't want to cooperate
with us at any sense." {name2} appears to the left of {name1} and
shrugs {hisher2} shoulders, showing {heshe2} don't understand what
made those people to think that way. "Okay, let's continue!" - you're
commanding... Understandable, trust is not often that days.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """{name1} and {name2} taking a direction to the tent camp
by your command. You're seeing them approaching the place and
speaking with inhabitants. After a couple of minutes of conversation
{name2} runs back to you, but {name1} continue to stand with two women.
{name2} jumps on the Train and explains: "No fighters, just several
females with children. They afraid of us, refusing to join, but me and
{name1} think we could give them a sack of coal. They are low on
resources." You silently nod, and {name2} takes a present for those
people. You're waiting for about 10 minutes, and both {name1} and
{name2} return back to you. "Good people" - {name2} finalizes.
"But very distrustful." "No wonder." - you're answering.
Single character can get Immunity""",
                        "effects": {"select_char": {"add_trait": "Immunity"}},
                    },
                    {
                        "score": range(80, 101),
                        "desc": """You're giving an order to {name1} and {name2} to move
to the tent camp and see if everything is alright there. Your people
getting to the place in minute, and you see them starting to speak
with the inhabitants. The campers looks calm and positive, so you're
relaxing a bit... After several minutes of talk, your people turn
back to the Train, but you also see one more person with them. They
getting closer to you, and {name1} explains: "Looks like we've found
a recruit. Do we have a free place?" Taking a quick gaze at the
newbie, you're starting to think if the team needs one more head.
One person can be recruited""",
                        "effects": {"recruit": 80},
                    },
                ),
            },
            {  # 2
                "name": "Lying Man",
                "type": "Meet",
                "class_weights": {"soldier": 10, "anarchist": 45, "raider": 28},
                "assignees": 1,
                "day_part_weights": {
                    "night": 0,
                    "morning": 4,
                    "noon": 8,
                    "evening": 10,
                },
                "desc": """Thinking about the Stench nature, you're absently looking around the
Train, when suddenly you find yourself gazing at a human body.
It almost blended with withered grass and is covered with snow -
seems, the man is dead. There is nothing around: no buildings,
signs of human, even trails... Probably, he died by himself...
It makes sense to take a look at him, who knows what can be found.
Deciding to make a walk, you're thinking who should you take as a
companion. Nothing promises troubles, so anyone should fit.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You're deciding to take {name1} as a companion for this small
walk. You both jump off the Train and take a direction to the body.
At some point you're noticing some kind of a movement. Is this
guy still alive? Or it's just a wind plays with the cape? {name1}
moves forward, and takes a seat near the body. Carefully, {heshe1}
turn over the man, and from under his corpse a mustard color
cloud rises suddenly. Not having time to react, {name1} inhales
it and jumps aside the body. "Oh, shit!" - {heshe1} inclines and
spits. "Faster, go for the doc!" - you're pushing {himher1} to
the Train and stopping your breath as well.
{name1} getting Weak Immunity""",
                        "effects": {"char_1": {"add_trait": "Weak immunity"}},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """You take your gun and turn your head to the locomotive deckhouse:
"{name1}, you're with me!". Like {heshe1} waited for these words,
{name1} walks out on air, and you both jump out of the Train. It
takes just a half of minute to approach the body, wrapped in a grey
cape. "Wait!" - {name1} uppers {hisher1} hand and points to some kind
of a small hills around the corpse. Interesting! {name1} lifts a stone
from the ground and throws it to the lying man. In the next moment
everything turns black, and you hear a terrible din. After several
seconds of emptiness, you're returning back to the reality. {name1}
gets up from the ground and shakes off. "That looks like a homemade
mine." - {heshe1} pronounces loudly. Fortunately, no one injured.
{name1} getting -10 health""",
                        "effects": {"char_1": {"health": -10}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """You're asking {name1} to follow you on this walk. Without
counter-arguments, {heshe1} takes {hisher1} gun and moves to the
right of you. The silent pause holds for some time. You know what is
the cause. "You're okay?" For a couple of seconds you think {name1}
won't answer, but {heshe1} does: "Yeah... yeah. My brother in the
better world now. I'm okay." At that point you're approaching the
lying body, taking a knee down near it and turn it over. The old
frozen corpse creaks. He's dead. A lack of wounds sais he indeed
died naturally, without someone's "help". No one looted the body,
but it anyway doesn't look like a rich source, so you're deciding
not to disturb the dead man. "Let's get back!" - you pronounce,
and you both taking a direction to the Train.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """You're commanding {name1} to gear up. In a couple of minutes
{heshe1} jumps off the Train and follows you in the lying body
direction. Fast approaching the spot, {name1} moves in front of
you and takes a knee sit near the man. "Dead, definitely." - {heshe1}
pronounces. - "It looks like he was travelling somewhere distant.
No supplies, no money, he doesn't even have warm clothes. Died here
alone." You're making a step towards {name1}: "These times no
one should be alone." {name1} stands up: "Good we have our own team"
- {heshe1} smiles to you. - "Thanks, you've brought us together."
Silently nodding, you point to the Train with your head.
Team cohesion +6""",
                        "effects": {"cohesion_gain": 6},
                    },
                    {
                        "score": range(80, 101),
                        "desc": """You're taking {name1} as a companion for this walk and
jumping off the Train. It takes a half of minute to get to the body.
Silently approaching to the man, {name1} inclines, then turns him over.
Surprisingly, you both see an old open-eyed face, covered with blood
and dirt. The man is alive! Making a step back, {name1} gazes at you.
The old man in the mean time starts to speak: "If it's in you, cut it
out! You better cut it out!" He uppers his hands and starts to shake
them - the sleeves goes down, unveiling his arms, covered with fresh
cuts. "When they'll got you, cut them out!" - he repeats. {name1} makes
a step towards you and silently pronounces: "We better leave him."
Taking a moment to overthink, you're deciding that it's a good idea,
this man is mad and most likely diseased. No way to help him.
Single character can get Masochism""",
                        "effects": {"select_char": {"add_trait": "Masochism"}},
                    },
                ),
            },
            {  # 3
                "name": "Assassin",
                "type": "Meet",
                "class_weights": {"soldier": 10, "anarchist": 15, "raider": 4},
                "assignees": 3,
                "day_part_weights": {
                    "night": 8,
                    "morning": 10,
                    "noon": 4,
                    "evening": 0,
                },
                "desc": """In the moment the Train stopped, you're finding your eyes on a dark
silhouette of an armed man. He doesn't seem to be aggressive, so
you're giving him some time to come closer. "Hey, guys!" - he says,
smiling. - "Nice to meet you, I may need some help." "We're listening" -
you answer. "Locals paid me to convince to deal with skinheads,
who camped in the nearby mine. There are a lot of those imbitsils,
so I'm gonna ask you to join me. I'll give you half of my lucre."
You're taking an attentive look at the man. He seems to be a pro,
well-armed, trained and cold blooded. Hitman probably. Doesn't look
like he's going to lure you into a trap - he could kill you much
easier, if he'd want. Than why not to give him a hand!?""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """Several hours passed since you've sent {name1}, {name2} and
{name3} to help the assassin, and you finally see your people walking
back to the Train. All three, they are covered with dirt and soot,
their clothes torn. Helping each other, they climb up to the locomotive,
and {name2} reporting: "We've entered the mine and started to shoot
skinheads one by one. But something went wrong, and we've been
littered with stones. It took us an eternity to dig out." "An
eternity!" - {name3} repeats, inclining {hisher3} head. {name2}
continues: "The hitman is dead we suppose." Ordering your people
to get clean and rest, you're commanding the machinist to take off.
{name2} and {name3} getting Fear of dark""",
                        "effects": {
                            "char_2": {"add_trait": "Fear of dark"},
                            "char_3": {"add_trait": "Fear of dark"},
                        },
                    },
                    {
                        "score": range(20, 40),
                        "desc": """{name1}, {name2} and {name3} following the hitman and go dark
for several hours. The lack of any signs of your people makes you
little bit nervous, but in some moment you see them returning back
to the Train. They all look tired and dirty, but no one seem to be
seriously injured. "No good news." - {name1} explains to you,
climbing up to the locomotive. - "There was tens of skinheads,
and we barely made it out there alive. Our new friend wasn't so
lucky." - {heshe1} sighs. - "We have a couple of scratches,
nothing serous." Well, at least everyone is in one piece; the
locomotive engine starts to warm up.
{name1}, {name2} and {name3} getting -10 health""",
                        "effects": {"assignees": {"health": -10}},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """You're sending {name1}, {name2} and {name3} with the smiling
assassin. After all, skinheads are the disease to be cured, no matter
if it is an end the world. A couple of hours passes, when you finally
see your people. They look neutral, and there are no the hitman
with them. Getting closer to the Train, {name3} explains what's
happened: "Those bastards were waiting for us. Our friend didn't
make it, and we barely made it out there ourselves." They all climb
up to the Train. "We better hurry up" - {name2} adds. - "Who knows,
they could have decide to follows us." Well, on that you all agree.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """You're sending {name1}, {name2} and {name3} with the hitman
as a support. They fastly disappear behind the hill, and two hours
passed, before they get on sight again. Throwing a gaze through
binoculars, you see that everyone is okay. The hitman is not with
your people. "We've finished them all." - {name1} says, getting closer
to the Train. - "The man gave us some money and vanished, like he
never been there." Climbing up to the Train, your messengers moving
each to his/her place. Well, the job is done, bad people were stopped,
and some money earned. Sounds like a lucky outing!
You're getting 100$""",
                        "effects": {"money": 100},
                    },
                    {
                        "score": range(80, 101),
                        "desc": """{name1}, {name2} and {name3} following the hitman as a
support. A couple of hours passes before you see your people again.
From 200 meters you can see that their campaign was successful -
they smile and actively discuss something. Getting closer to you,
{name1} start to describe you the details of the operation, others
joining him. "This guy was like a shadow!" "{name2} shooted three
bastards in a second!" "We've been moving like a single one person."
The hotly told history sounds to you like a battle to remember!
Everyone done something, the vespiary burned to the ground, and
every messenger is very impressed by the hitman skills.
You're getting 100$
Single character can get Fast hands""",
                        "effects": {
                            "select_char": {"add_trait": "Fast hands"},
                            "money": 100,
                        },
                    },
                ),
            },
            {  # 4
                "name": "New Outpost",
                "type": "Meet",
                "class_weights": {"soldier": 10, "anarchist": 45, "raider": 25},
                "assignees": 1,
                "day_part_weights": {
                    "night": 0,
                    "morning": 3,
                    "noon": 7,
                    "evening": 10,
                },
                "desc": """From a big distance you're catching your eyes on a small building,
near which a lot of people silhouettes are looming. Getting closer, you
see a lot of construction equipment, and the building itself looks like
a small outpost, still in construction progress. Concrete walls, a couple
of bases for towers, big metal gates... Workers, hearing the Train
engine, directing their gazes at you, without any sign of aggression.
Definitely, they are not skinheads, but their uniform and equipment
seems to be in a very good shape - aren't they came here by government
request? It's worth sending a messenger to have a word with them at
least. Maybe they have some valuable info about the situation in the
country, or just nearby lands!?""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You're listing the team within mind, and decide to send {name1}.
Without delays, {heshe1} grabs {hisher1} gun and walks to the construction
sight. You take your binoculars and point it to your fighter. Nothing
wrong seems to be happening, {name1} simply speaks with two workers,
but suddenly you hear a loud crash. Gazing the place to which workers
run, you see a man pinned down by a big metal object: dark red blood
spreads all around him, his shouts tear the air. Moving the binoculars
away, you see {name1} running back to the Train. "They build new
outpost to hold skinheads spreading." - {heshe1} says, climbing up to
the locomotive. You see that {hisher1} eyes are open wide, and the skin
became pale. "You're okay?" Turning head to you, {name1} keeps silent
for a second... "Yes. I guess. Just..."  - {heshe1} looks at the outpost.
{name1} getting Hemophobia""",
                        "effects": {"char_1": {"add_trait": "Hemophobia"}},
                    },
                    {
                        "score": range(20, 40),
                        "desc": """{name1} seems to be a good candidate for the task, so you're
giving {himher1} an order to speak with those people. Jumping off to
the ground, {heshe1} goes to the construction sight and speaks with
workers for some time... Does one more weaponized camp protect
from the Stench? Probably, not, still, they are building it... You
see {name1} giving something to the workers, and next turns back.
Jumping back to the Train, {heshe1} explains: "These people are trying
to build their own stronghold, for those, whom nearby cities doesn't
want to invite. I've gave them some money, 'cause it looks like a good
idea for me." - {name1} throws a gaze to the construction sight. Well,
who knows, who knows, this idea can also be completely useless.
You losing 40$""",
                        "effects": {"money": -40},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """{name1} seems to be an appropriate person to speak with
workers, so you're sending {himher1} to the construction sight. It takes
ten minutes for {himher1} to get there and to speak with a couple of
workers with dirty faces and orange uniform. Nothing wrong happening,
so you're sitting down to your chair, waiting for {name1} to return.
Entering the deckhouse, {heshe1} gets closer to you: "Well, they are
building a new outpost to hold skinheads in this region. The nearby
city supports this project, so I suppose they are in better condition
than we are." Nodding your head, you're giving an order to start engine.
At least that means the next city is a good place for a stop.""",
                        "effects": {},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """Running through the team list, you're deciding to send {name1}
for negotiations. Energetically {heshe1} takes {hisher1} gun and directs
to the construction sight, but in the next minute a couple of
workers are moving out of the outpost, towards {name1}. Getting
closer to each other, {name1} and workers exchange handshakes, and
all three going to the locomotive. You see that builders' faces become
more interested with every step. "Wow, what a beautiful machine you
have!" - one of them pronounces. - "That's actually a stronghold on
wheels!" Both workers get closer and view the locomotive. "That's
incredible!" - the same man proclaims. - "You're very lucky to get
your hands on it!"... After several minutes of talk the workers turn
back to their outpost, but the jealous words still make you proud.
Team cohesion +6""",
                        "effects": {"cohesion_gain": 6},
                    },
                    {
                        "score": range(80, 101),
                        "desc": """You're deciding to send {name1} to negotiate with workers.
Jumping to the ground, {heshe1} moves to the spot, and sees that one
of the builders went out of the outpost towards {himher1}. After a
minute of talking {name1} figures out that these people are building
a new outpost to hold skinheads in this region. The worker asks {name1}
to follow him, and they both go to the opposite side of the camp. There
your messenger sees a lot of dead bodies laid out in rows - about
forty men. "These are skinheads bastards we already stopped here."
- the worker brags. "Looks significant!" - {name1} answers and means
it. It's really significant to clear so much filth. "Right, I have to
return to my people" - {heshe1} takes leave of the constructor and,
throwing the last gaze at bodies, takes a direction to the Train.
Single character can get Bloodthirsty""",
                        "effects": {"select_char": {"add_trait": "Bloodthirsty"}},
                    },
                ),
            },
            {  # 5
                "name": "Cargo Column",
                "type": "Meet",
                "class_weights": {"soldier": 5, "anarchist": 22.5, "raider": 12.5},
                "assignees": 2,
                "day_part_weights": {
                    "night": 0,
                    "morning": 10,
                    "noon": 7,
                    "evening": 3,
                },
                "desc": """For the last ten minutes you've been observing a road, which turned
to the railway and has been following it in a straight parallel. A lot of
pits and cracks showing that the road isn't very well maintained, most
likely it's really old. Still, in the next minute you see a big column,
staying on the grey concrete: bus, several big trucks, filled with
different stuff, such as furniture, metal and garden inventar, and a
couple of smaller cars. Several heavy machine guns and at least ten
weaponized men are complementing the picture. The beholders doesn't
look like a thugs, so it's probably makes sense to speak with them.
Maybe they have something to trade or exchange.""",
                "results": (
                    {
                        "score": range(0, 20),
                        "desc": """You decide that {name1} and {name2} will be a party - those
people are armed after all. You fighters climb down from the Train
and direct to the cars. Getting closer, they start to speak with
column defenders, and in some moment they both move up their guns
and start to shoot. Car column spurts away in the same second, which
is strange, as they had more people than you. Still, your messengers
returning back to you, both with light wounds. Climbing to the
locomotive, {name1} explains: "Marauders, taking the stuff out of
the regions covered with the Stench. Stealers in the other words."
- {heshe1} takes a look at {hisher1} wound on the left shoulder. - "I'll go
find the doctor." Gazing at smoke clouds, you think how organized
and weaponized the marauders are. Seems a big business.
{name1} and {name2} getting -20 health""",
                        "effects": {
                            "char_1": {"health": -20},
                            "char_2": {"health": -20},
                        },
                    },
                    {
                        "score": range(20, 40),
                        "desc": """You choose {name1} and {name2} to negotiate with the column men.
They both carefully getting closer to the cars and start to speak with
a big guy in a cap. You're analyzing the column itself: well-armed
people, cargo cars, good organization - all the signs of professionals,
still, they doesn't show any aggressive intentions. Several more
minutes passes, and your people turning back to the locomotive. The
car column starts the engines. {name1} and {name2} getting closer to
you: "So, they are government people, transporting cargoes and people
between several cities. Trying to do whatever they can to help folks
in the country." Okay then, it's not a bad piece of news. Good to see
that rulers are still in a strive, together with people.""",
                        "effects": {},
                    },
                    {
                        "score": range(40, 60),
                        "desc": """{name1} and {name2} taking a direction to the cars column by your
order. While they are getting closer to the big man walking to meet
them, you're analyzing the cortege: a lot of cargo, a lot of guns,
and... a lot of refugees!? You didn't see them at the first minute,
they probably were hiding, but now started to peek out. Dirty, ragged,
different aged... You patiently wait for your people to figure out
the details. You see them taking something from the big man, and
turning back to the locomotive. "This is a help from a local city -
they transporting people away from the Stench clouds." - {name2}
tells, entering the deck house. - "They kindly gave us some of their
medicine." - {heshe2} puts a small white box on the table. Well,
that's actually very kind of them!
Single character can get +30 health,""",
                        "effects": {"select_char": {"health": 30}},
                    },
                    {
                        "score": range(60, 80),
                        "desc": """You make a decision to send {name1} and {name2} for a speak. They
take their guns and carefully go to the machines, while a couple of men
move towards them from their side. After several seconds of talk
{name1} and {name2} taking their guns away and follow the men. Trying
to get what's happening, you see your messengers helping column
guys to pull up a big metal object, probably fallen out of the truck.
Is it why they stopped? Looking at smiling fighters, telling goodbye
to your people, you see that yes, it is. While their cars start to
move, {name1} and {name2} come closer to you, telling: "Positive guys!
Transporting people away from the Stench. Asked to help them a
little and gave us this" - {name2} puts some dollars to the table.
You're getting +90$
One character can get Liberal""",
                        "effects": {
                            "money": 90,
                            "select_char": {"add_trait": "Liberal"},
                        },
                    },
                    {
                        "score": range(80, 101),
                        "desc": """You're sending {name1} and {name2} to negotiate with the column
guys. They carefully approaching the men, and starting to talk.
Several minutes passed, and then you see a silhouette jumping out of
the bus and following your people. What does it mean? "Hey, captain!"
- {name1} says loudly. - "These are refugees transportation party, came
from the nearby city to help people to get out of the Stench. No any
problem with them, but there is a recruit, who wants to join us. What
will you say?" You're viewing the candidate from high to down. Well,
that is something to carefully think about.
One person can be recruited""",
                        "effects": {"recruit": 60},
                    },
                ),
            },
        ),
    },
}
