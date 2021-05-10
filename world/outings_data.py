"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Outings scenarios and effects.
"""

ENEMY_CAMP = [
    {  # 1
        "name": "Car Column",
        "type": "Enemy Camp",
        "class_weights": {"soldier": 13.3, "raider": 4, "anarchist": 6},
        "assignees": 3,
        "day_part_weights": {"night": 10, "morning": 0, "noon": 3, "evening": 8},
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
Adjutant getting -80 durability""",
                "effects": {"train": {"durability": -80}},
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
You're getting 90$""",
                "effects": {"money": 90},
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
You're getting 100$ and 1 stimulator
{name1} getting -15 health""",
                "effects": {"money": 100, "stimulators": 1, "char_1": {"health": -15}},
            },
        ),
    },
    {  # 2
        "name": "Big Tent",
        "type": "Enemy Camp",
        "class_weights": {"soldier": 40, "raider": 20, "anarchist": 9},
        "assignees": 1,
        "day_part_weights": {"night": 0, "morning": 10, "noon": 6, "evening": 4},
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
You're getting 70$""",
                "effects": {"money": 70},
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
You're getting 100$""",
                "effects": {"money": 100},
            },
        ),
    },
    {  # 3
        "name": "Bus",
        "type": "Enemy Camp",
        "class_weights": {"soldier": 20, "raider": 6, "anarchist": 12},
        "assignees": 2,
        "day_part_weights": {"night": 0, "morning": 3, "noon": 10, "evening": 7},
        "desc": """The big red two-storied bus standing at the middle of the meadow
catches your attention from a very long distance. Bringing the binoculars
to your eyes, you're seeing that it's little bit old and shabby, but sand
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
                "effects": {"char_1": {"health": -35}, "char_2": {"energy": -20}},
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
and then suddenly falls silent. Adjutant getting -40 durability""",
                "effects": {"train": {"durability": -40}},
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
car, your people start to rummage through it, swinging the old metal
carcass. While it all happening, you're seeing a big jeep on a horizon.
Whistling loudly to your people, you're preparing for a fight. It takes
two more minutes for {name1} and {name2} to jump outside the bus. The
gang in the jeep, approaching fast, are starting to shoot, and you're
opening fire back. {name1} and {name2}, using your cover shooting, are
returning back to the Train with several banknotes, and you're
deciding to move along before the bus beholders came too close.
You're getting 80$""",
                "effects": {"money": 80},
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
You're getting 100$""",
                "effects": {"money": 100},
            },
        ),
    },
    {  # 4
        "name": "Gas Station",
        "type": "Enemy Camp",
        "class_weights": {"soldier": 20, "raider": 7, "anarchist": 12},
        "assignees": 2,
        "day_part_weights": {"night": 4, "morning": 5, "noon": 10, "evening": 2},
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
{name1} getting -40 health
{name2} getting -10 health""",
                "effects": {"char_1": {"health": -40}, "char_2": {"health": -10}},
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
                "effects": {"char_1": {"health": -10}, "char_2": {"health": -10}},
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
Getting closer to the building, they hear music, and see three people
within. In the next moment from the other side of the station four
skinheads with guns are appearing, with clear intent to attack the
gas point. {name1} and {name2}, not yet detected by robbers, upper their
guns and shooting off all of these cruds. The station dwellers moving
outside the building to see what's happening, and understand that your
people saved them from skinheads. They applaud {name1} and {name2},
speaking of weird language unfamiliar to your messengers. {name1} and
{name2} nod their heads, turning back to the Train, but one of the
dwellers stops them and gives them several dollar banknotes.
You're getting 80$""",
                "effects": {"money": 80},
            },
            {
                "score": range(80, 100),
                "desc": """{name1} and {name2} fastly moving to the gas station. Getting
closer, they slow down, but after several seconds they see that the
building is abandoned. The glass door is open, music is still playing,
but dust lies everywhere and silence fills the air. {name1} and {name2}
together walking around the station, enter it and, seeing no threats,
splitting to check two places simultaneously: the cash and the storeroom.
Cash machine, fortunately, is open, and {name2} finds a toolbox really
fast. Energetically taking their lucky catches, {name1} and {name2} in
a good mood returning back to the Train.
You're getting 90$ and +100 Adjutant durability""",
                "effects": {"money": 90, "durability": 100},
            },
        ),
    },
    {  # 5
        "name": "Trailers",
        "type": "Enemy Camp",
        "class_weights": {"soldier": 13.3, "raider": 4, "anarchist": 9},
        "assignees": 3,
        "day_part_weights": {"night": 10, "morning": 0, "noon": 4, "evening": 7},
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
{name3} finds 40$ in there. With this find your messengers return back.
You're getting 40$""",
                "effects": {"money": 40},
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
        "class_weights": {"soldier": 13.3, "raider": 10, "anarchist": 5},
        "assignees": 3,
        "day_part_weights": {"night": 0, "morning": 2, "noon": 6, "evening": 10},
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
Adjutant durability -60""",
                "effects": {"train": {"durability": -60}},
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
        "class_weights": {"soldier": 20, "raider": 12, "anarchist": 5},
        "assignees": 2,
        "day_part_weights": {"night": 0, "morning": 5, "noon": 10, "evening": 7},
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
    {  # 8
        "name": "Kid's camp",
        "type": "Enemy Camp",
        "class_weights": {"soldier": 40, "raider": 20, "anarchist": 9},
        "assignees": 1,
        "day_part_weights": {"night": 10, "morning": 7, "noon": 0, "evening": 3},
        "desc": """From a big distance you've noticed several dark green buildings. Got
closer, you see that they are old, but still in a good shape. A bunch of
colorful attractions makes you think that this is a summer camp for kids.
There are no kids, however, but the place is definitely inhabited, most
likely by skinheads - you see bodies lying here and there, smoke rising
from a couple of buildings and a lot of fresh litter. It looks like
the current owners of the camp didn't notice your arrival, so it makes
sense to send just one scout for a quet place recon.""",
        "results": (
            {
                "score": range(0, 20),
                "desc": """You're sending {name1} for a scouting. Without delays {heshe1} takes
the direction to the camp and silently approaches it. The place seems
quiet for some time, but suddenly several doors are opening, and shots
are tearing the air. Felling to the ground, {name1} start to shoot
all around, and you're trying to help {himher1} from the Train. It takes
about three minutes for your messenger to get back to you, but the
skinheads doesn't want to leave you be - they run to the locomotive
with loud shouts. Lucky for you, they didn't think about getting into
open place until it became too late. Your coordinated fire drops them
one by one. Making a quick roll call, you understand that you all,
however, got some wounds during this skirmish.
All of your teammates are getting -30 health""",
                "effects": {"all": {"health": -30}},
            },
            {
                "score": range(20, 40),
                "desc": """You're choosing {name1} as a scout. Jumping to the ground, {heshe1}
puts on a hood against the cold wind and walks to the spot. It takes
a couple of minutes for your messenger to understand that the camp is
forsaken, not long ago though. Walking around, {heshe1} tries to find
something useful, but nothing except empty backpacks and clothes
shows up. In some moment a strong wind gust swepts in the air, and
{name1} hear a metal creak. Uppering {hisher1} head, {heshe1} see that big
metal water storage, standing in the middle of the camp, leans
over, and in the next second fails to the ground. Dirty water rises
between the buildings, and {name1} spurts back to the locomotive. Wet
and cold, {heshe1} jumps to the Train and runs into the deck, closer
to the engine to get warm faster.
{name1} getting -30 energy""",
                "effects": {"char_1": {"energy": -30}},
            },
            {
                "score": range(40, 60),
                "desc": """You're deciding to send {name1} alone to take a look at the camp.
Grabbing {hisher1} gun, {heshe1} runs to the spot and starts to quetly
walk through the green buildings. It seems like the camp is forsaken
not very long ago - empty backpacks, clothes, some photos - the usual
stuff for a kid's camp, but nothing really useful while you're on a
road. Having examined three buildings, {name1} walks to the street
and feels a cold wind blowing. Not wanting to stay longer in such a
weather, {heshe1} takes a direction back to the locomotive: there is
nothing valuable in this place anyway.""",
                "effects": {},
            },
            {
                "score": range(60, 80),
                "desc": """By your command, {name1} prepares for a walk and jumps to
the ground. Getting closer to the camp, {heshe1} sees several skinhead
sentries. That, however, doesn't scare your messenger and {heshe1} sneaks
into the building with a red cross. It appears to be not just a medical
structure, but also a weapon storage. Throwing a gaze at the
containments, {name1} notices a big first aid kit and moves to it.
Several syringes, paper boxes of tablets, white bandages - {name1}
takes the whole kit and moves out of the building. Carefully walking
out of the camp aside of the watch, {heshe1} runs to the locomotive
and proudly enters the deck house with {hisher1} rich catch.
All of your teammates getting +20 health""",
                "effects": {"all": {"health": 20}},
            },
            {
                "score": range(80, 100),
                "desc": """{name1} becomes your messenger on this operation. Grabbing
{hisher1} stuff, {heshe1} silently jumps down to the ground and moves
into the camp. Only a couple of skinhead sentries lazily walk
around the buildings, talking loudly. Without a single effort
{name1} sneaks into the camp and penetrates into the wooden building,
which looks pretty much like a storage. Inside {heshe1} sees so many
different things that it becomes really hard to tell, what is actually
stored in here. Jewelry, money, paintings, sculptures - it looks like
skinheads are robbing everyone around and store the catch here. It's
a pirate treasure really! Hearing some kind of a fuss on the street,
{name1} grabs several small things, lying closely, and silently exits
the building to take a direction to the locomotive.
You're getting 130$""",
                "effects": {"money": 130},
            },
        ),
    },
    {  # 9
        "name": "Auto Repair",
        "type": "Enemy Camp",
        "class_weights": {"soldier": 40, "raider": 20, "anarchist": 9},
        "assignees": 1,
        "day_part_weights": {"night": 10, "morning": 0, "noon": 4, "evening": 7},
        "desc": """An old highway, stretched out to the left of the railway, has taken your
attention, and your supervision at some moment pays off: you see an
auto repair shop. It's small, just three car places without utility
rooms, but it's still something. Roller shutters are all closed,
window glasses are intact - everything says the place is over watched
by someone. It makes sense to send a scout to take a closer look at
the building. It's an auto repair shop after all, meaning there
should be tools, which can be used for the locomotive maintenance.""",
        "results": (
            {
                "score": range(0, 20),
                "desc": """You're sending {name1} to the auto repair shop for a closer look.
While your messenger approaches the building, you notice some kind
of a movement inside it - shadows slide near windows, but nothing
promises troubles so far. You do a loud whistle and show {name1}
that it's better to stay sharp. Nodding {hisher1} head, {heshe1} slows
a little and moves further with more caution. Suddenly all three
roller shutters explode, and orange fire mushrooms break out of
the building. Shock wave knocks {name1} down to the ground, and
makes locomotive windows shaking. Getting up, {name1} runs back
to you, while you're observing the auto shop burning remnants.
Seems like something gone terribly wrong inside it...
{name1} getting Nervousness""",
                "effects": {"char_1": {"add_trait": "Nervousness"}},
            },
            {
                "score": range(20, 40),
                "desc": """{name1} takes {hisher1} gun and moves to the auto repair shop by your
command. On the middle of {hisher1} way the right roller shutter
moves up with a loud bolt, and a couple of men start to shoot at
your messenger. You upper your gun and cover {name1}. Just several
seconds of shooting, and both of the rivals fall to the ground. With
caution {name1} continue the way, but suddenly an explosion tears
the shop, throwing its plastic and metal walls to all sides at
once. {name1} falls to the ground because of the shock wave, but
gets up in the next seconds. Looks like no serious wounds happened.
While {heshe1} returns back to the locomotive, you're thinking if
there were more people and they decided to explode
themselves, or it is just an occasional catastrophe?
{name1} getting -25 health""",
                "effects": {"char_1": {"health": -25}},
            },
            {
                "score": range(40, 60),
                "desc": """{name1} takes a direction to the auto repair shop. You're tracking
{himher1} from the locomotive. Silently your messenger gets closer and
opens a roller shutter. Nothing happens, no shooting, no people
appearing, looks like the building is abandoned already. {name1}
carefully enters inside and disappears from your gaze for at least
ten minutes. You're becoming nervous little by little, but finally
{heshe1} exits the shop. You see nothing in {hisher1} hands, and,
climbing to the locomotive, your messengers confirms your
thoughts - there was nothing. Someone already looted the
building, taking every-single-thing useful.""",
                "effects": {},
            },
            {
                "score": range(60, 80),
                "desc": """{name1}, following your command, takes {hisher1} gear and walks
to the auto repair shop. Getting closer to the building, {heshe1} opens
a roller shutter and enters inside. For some time silence flies in the
air, but suddenly you hear shots. Three, four-five, six... A couple of
seconds passes, and you see {name1} in the entrance arch, showing you
that everything is okay. Disappearing in the shop inners, {heshe1} returns
back after a half of minute with a big metal box. Tools, ha?! You're
commanding others to help {himher1} with the catch, while you're
listing the parts of the locomotive, which should be given an
engineering attention in the first place.
Adjutant durability +70""",
                "effects": {"train": {"durability": 70}},
            },
            {
                "score": range(80, 100),
                "desc": """{name1} takes {hisher1} gun and, following your command, walks
towards the auto repair shop. It's clear that someone is in there:
through the window you see shadows moving inside. {name1} see them
as well, so {heshe1} makes a circle around the shop and climbs to
its roof. Ceiling windows make it possible for {himher1} to drop
the ambushing skinheads even before they understood who's firing.
Climbing down and entering the shop, {name1} walks out with someone
else. When close enough to the locomotive, {heshe1} explains:
"There was a hostage there. Thought maybe we can give a ride."
Looking at your scout's companion, you evaluate a possible recruit.
One person can be recruited""",
                "effects": {"recruit": 70},
            },
        ),
    },
]

LOOTING = [
    {  # 1
        "name": "Abandoned Car",
        "type": "Looting",
        "class_weights": {"soldier": 20, "raider": 40, "anarchist": 9},
        "assignees": 1,
        "day_part_weights": {"night": 0, "morning": 3, "noon": 10, "evening": 5},
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
and, opening it, {name1} sees that it contains several not overdue meds!
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
Adjutant durability +100""",
                "effects": {"train": {"durability": 100}},
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
        "class_weights": {"soldier": 6, "raider": 20, "anarchist": 13},
        "assignees": 2,
        "day_part_weights": {"night": 0, "morning": 7, "noon": 10, "evening": 3},
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
                "effects": {"char_1": {"energy": -30}, "char_2": {"energy": -30}},
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
old photos. Finding nothing, {name1} decides to take a look at the tent
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
        "class_weights": {"soldier": 9, "raider": 13.3, "anarchist": 3},
        "assignees": 3,
        "day_part_weights": {"night": 8, "morning": 2, "noon": 5, "evening": 10},
        "desc": """Called by one of your teammates, you're walking out of
the cabin and in the same moment seeing an old hut not far from the
railway. Putting binoculars to your eyes, you're looking at it with good
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
                "desc": """{name1}, {name2} and {name3} are gearing up and taking direction
to the hut. Approaching to it they see that wood building is long
abandoned: weeds are crossing the door, windows are broken, and
stillness fills the air. {name2} and {name3} are moving into the house, while
{name1} is standing outside on a watch. It takes a lot of time for {name3}
to check all the broken furniture in the first room, but {heshe3} finds
nothing. {name2} appears to become more lucky: {heshe2} managed to
find 50$ within a lady's old bag. With such a results {name2} and
{name3} are leaving the silent and dusty house, and joining {name1}
to get back to Train and others.""",
                "effects": {"money": 50},
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
Adjutant durability +100""",
                "effects": {"train": {"durability": 100}},
            },
        ),
    },
    {  # 4
        "name": "Monastery",
        "type": "Looting",
        "class_weights": {"soldier": 9, "raider": 13.3, "anarchist": 4},
        "assignees": 3,
        "day_part_weights": {"night": 10, "morning": 2, "noon": 5, "evening": 8},
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
this noise they hear human voices, and they are many. Lifting up, {name3}
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
soon they see it's completely forsaken long time ago. Entering inside,
they find a lot of wood wreck. Air smells mold and dust, strong silence
soar in the old monastery. Walking along the building, your people
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
        "class_weights": {"soldier": 7, "raider": 20, "anarchist": 14},
        "assignees": 2,
        "day_part_weights": {"night": 2, "morning": 4, "noon": 10, "evening": 8},
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
Adjutant durability +50""",
                "effects": {"train": {"durability": 50}},
            },
            {
                "score": range(40, 60),
                "desc": """You're sending {name1} with {name2} to take a look
at the crash site. {name2} takes a big backpack in hope there will be
something to bring back. Both they are moving to the damaged truck
and starting to search through the plastic boxes scattered around the
place. At the first minute they understand that someone already emptied
every container at the place, probably, the same one who attacked the
truck - they see a lot of sleeves, shot holes and some blood spots.
Taking a look inside the car cabin, {name2} finds that it wasn't looted
somewhy, and there is a small black plastic box with several syringes
inside. Gazing at the label carefully, {name2} understands that it's
some kind of a not very legal doping. Well, it's still something!
You're getting 1 stimulator""",
                "effects": {"stimulators": 1},
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
        "class_weights": {"soldier": 4, "raider": 13.3, "anarchist": 10},
        "assignees": 3,
        "day_part_weights": {"night": 5, "morning": 7, "noon": 10, "evening": 2},
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
likely was long forsaken. {name1}, rubbing {hisher1} forehead, warmed up by
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
Adjutant durability +100""",
                "effects": {"train": {"durability": 100}},
            },
        ),
    },
    {  # 7
        "name": "Silo",
        "type": "Looting",
        "class_weights": {"soldier": 6, "raider": 20, "anarchist": 13},
        "assignees": 2,
        "day_part_weights": {"night": 10, "morning": 0, "noon": 3, "evening": 5},
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
    {  # 8
        "name": "Wooden Barn",
        "type": "Looting",
        "class_weights": {"soldier": 20, "raider": 40, "anarchist": 9},
        "assignees": 1,
        "day_part_weights": {"night": 7, "morning": 0, "noon": 3, "evening": 10},
        "desc": """Gazing at the horizon line, you've been overlooking corn fields
for the last two hours. But suddenly you see a big dark wooden
barn, standing on the edge of the green field, a little covered
with snow. Large entrance gates are opened, but lack of chains and
locks makes you think it was never actually closed. So, it can be
a good place for looting as well as just an empty building. Who
should be sent to clarify the situation?""",
        "results": (
            {
                "score": range(0, 20),
                "desc": """{name1}, chosen as your messenger, takes {hisher1} gear
and runs to the barn fast. You're staying sharp, looking at the
nearlands very careful, but nothing promises any troubles. Entering
the barn in the meantime, {name1} sees several old naked bodies,
hanged from the ceiling. Big numbers of bruises and dry blood
saying that these people were tortured. Moving {hisher1} eyes out
of the terrible sight, {name1} walks to the table, covered with
different stuff. Passports. Opening them one by one, {name1} sees
that all of them are foreign. Looks like this place belonged to
skinheads, and here they were killing those, who came from abroad.
Throwing the last gaze at the hanged, {name1} exits the barn.
{name1} getting -35 energy""",
                "effects": {"char_1": {"energy": -35}},
            },
            {
                "score": range(20, 40),
                "desc": """You're sending {name1} to recon the old building.
Jumping off the locomotive, {heshe1} takes a direction to the barn,
but in the next moment you see a fire flash in the gates opening.
A big rocket with a loud hiss flies in the direction of the train
and explodes just in a couple of meters aside of its wheels. {name1}
makes several shots, and in the next second a man in a brown coat
falls from behind the gates. You're nodding to {name1}, permitting
{himher1} to take a look at the barn. Jumping off the locomotive,
you're observing the wheels: damage doesn't seem very serious, still,
it's damage. {name1} in the meantime exits back, showing that
there was nothing interesting inside the wooden barn.
Adjutant getting -60 durability""",
                "effects": {"train": {"durability": -60}},
            },
            {
                "score": range(40, 60),
                "desc": """As the barn doesn't seem to be very inhabited
and it stands very close to the railway, you're deciding to send
{name1} just alone. Not poking around too long, {heshe1} runs to
the building, enters it and observes emptiness. It's clear that
owner took everything useful and flew away. The only strange
detail is several horse skeletons. They were left here, on leashes,
and now seem to be dead for a very long time. Not the most humane
decision! Still, we don't know what actually happened here, maybe
it's not what it looks like. Anyway {name1} returns back empty.""",
                "effects": {},
            },
            {
                "score": range(60, 80),
                "desc": """{name1}, chosen as your messenger, takes {hisher1}
gear and moves to the old barn. Quetly entering the building, {heshe1}
sees several horse skeletons on a leashes; the place seems to be not
looted, so it can be said the owner leaved the barn in a hurry.
Walking around, {name1} catches {hisher1} eyes on an aid kit. It looks to be
intended for animals, but inside {name1} finds several syringes that
can be also useful for humans. Nothing more attracts your messenger
attention, so {heshe1} takes medicines and returns back to the Train.
Single character can get +30 health""",
                "effects": {"select_char": {"health": 30}},
            },
            {
                "score": range(80, 101),
                "desc": """{name1}, driven by your command, jumps to the ground and
moves to the wooden barn. Nothing promises troubles, so {heshe1} enters
inside and starts to rummage through the old stuff. The place doesn't
seem looted, but all the things are really ancient - horse leashes, rusty
tools, dark blue cloth pieces... The owner probably was a jockey - {name1}
see several saddles and a blue jockey suit. Almost without hope your
envoy opens a first aid kit and finds a horse doping there. Hm-m, it
can be diluted and used for people as well. {name1} decides to take
the syringe and go back to the train, as there is nothing more in here.
You're getting 2 stimulators""",
                "effects": {"stimulators": 2},
            },
        ),
    },
    {  # 9
        "name": "Refugees Camp",
        "type": "Looting",
        "class_weights": {"soldier": 9, "raider": 40, "anarchist": 19},
        "assignees": 1,
        "day_part_weights": {"night": 0, "morning": 7, "noon": 10, "evening": 4},
        "desc": """From at least 500 meters you've caught your eyes
on some kind of a rubbish pile. Dark cloth pieces, black heaps of
bonfires and several colored plastic boxes... Getting closer to the
place, you understand, that it was a temporary camp, most likely
of foreigners, who came to Silewer in search of a shelter. Well,
that makes sense to take a look at the place, maybe something
useful left there. One messenger should be enough.""",
        "results": (
            {
                "score": range(0, 20),
                "desc": """You decide to send {name1} into the camp for a recon of
the place. As the nearlands are very open, only several trees
obstruct the gaze, you don't expect any troubles. {name1} gets
closer to the camp remnants, inclines and starts to rummage through
the things scattered around. Nothing attracts {hisher1} attention
for a very long time: empty cans, plastic bottles, cling film, and
nothing interesting. But in some moment {heshe1} sees a big cauldron,
covered with metal cap. Unlikely it's worth checking, but {name1}
opens it, and recoils in the same second - a vile cloud of rotten
food flyes from under it. Coughing wildly, {name1} turns back to
you. It appears, the things left in the cauldron was so ancient
that became even little bit poisonous.
{name1} getting -25 health.""",
                "effects": {"char_1": {"health": -25}},
            },
            {
                "score": range(20, 40),
                "desc": """You're choosing {name1} as a messengers for this recon.
Without delays, {heshe1} takes {hisher1} gun and jumps down to the ground.
The pale grass, covered with water because of the cold air and the
locomotive warmth faced with each other, appears to be very slippery.
{name1}, touching it with {hisher1} legs, loses balance, and falls to
the ground. You see several papers flying out of {hisher1} pocket, and
by wind blowing raise up really fast. {name1} gets up, and you try to
find the loss with your eyes, but looks like the papers flew away.
Recounting {hisher1} money, {name1} pronounces sadly: "Thirty dollars!
It's about thirty dollars just got lost in wind."
You're losing 30$""",
                "effects": {"money": -30},
            },
            {
                "score": range(40, 60),
                "desc": """You're sending {name1} for a fast overview of the camp
remnants. Taking the gun, {heshe1} jumps off the locomotive, and runs
to the place. It looks like someone attacked the refugees, as there
are several dark red blood spots on the grass, and bullet liners are
shining here and there. There are no bodies, but if there was something
useful in this place, it's already taken. Making a couple of circles
around and carefully looking at what's left, just for sure, {name1}
takes direction back to the locomotive. Nothing interesting.""",
                "effects": {},
            },
            {
                "score": range(60, 80),
                "desc": """After a short overthinking you decide to send {name1} to
take a closer look at the refugees camp remnants. Carefully watching
around, {heshe1} walks to the place. It appears there was a skirmish in
here: {heshe1} sees bullet liners and even a round of a scorched grass.
A grenade explosion, ha? There are also several bodies, skinheads and
others. The camp was left in a hurry, so {name1} starts to rummage
through the stuff scattered around. After several minutes of a search
{heshe1} finally see a personal pocket aid kit. Opening it, {name1}
finds a tiny syringe of a painkiller, water clearing tablets and
even more. That's actually a good catch!
Single character can get +25 health and +20 energy""",
                "effects": {"select_char": {"health": 25, "energy": 20}},
            },
            {
                "score": range(80, 101),
                "desc": """You make a decision to send {name1} for the place recon.
Without long preparations {heshe1} moves to the camp. Getting closer,
{heshe1} finds a lot of bullet liners, blood spots, but no bodies. It seems
like there was a skirmish, but refugees successfully left. {name1} starts
to observe things remaining at the place. Just a couple of seconds
makes it clear that the camp dwellers left all the heavy equipment and
tools. Inspired, {name1} takes the most valuable things and returns
to the locomotive to ask others to join. In three runs you and your
people take almost everything useful from the camp.
Adjutant durability +100""",
                "effects": {"durability": 100},
            },
        ),
    },
]

MEET = [
    {  # 1
        "name": "Tents",
        "type": "Meet",
        "class_weights": {"soldier": 5, "anarchist": 20, "raider": 13},
        "assignees": 2,
        "day_part_weights": {"night": 0, "morning": 10, "noon": 7, "evening": 4},
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
        "class_weights": {"soldier": 10, "anarchist": 40, "raider": 22},
        "assignees": 1,
        "day_part_weights": {"night": 0, "morning": 4, "noon": 8, "evening": 10},
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
Crew cohesion +6""",
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
        "class_weights": {"soldier": 8, "anarchist": 13.3, "raider": 4},
        "assignees": 3,
        "day_part_weights": {"night": 8, "morning": 10, "noon": 4, "evening": 0},
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
                "effects": {"select_char": {"add_trait": "Fast hands"}, "money": 100},
            },
        ),
    },
    {  # 4
        "name": "New Outpost",
        "type": "Meet",
        "class_weights": {"soldier": 10, "anarchist": 40, "raider": 21},
        "assignees": 1,
        "day_part_weights": {"night": 0, "morning": 3, "noon": 7, "evening": 10},
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
You're losing 40$""",
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
Crew cohesion +6""",
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
        "class_weights": {"soldier": 5, "anarchist": 20, "raider": 12.5},
        "assignees": 2,
        "day_part_weights": {"night": 0, "morning": 10, "noon": 7, "evening": 3},
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
                "effects": {"char_1": {"health": -20}, "char_2": {"health": -20}},
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
                "effects": {"money": 90, "select_char": {"add_trait": "Liberal"}},
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
    {  # 6
        "name": "Ill Deer",
        "type": "Meet",
        "class_weights": {"soldier": 3, "anarchist": 13.3, "raider": 7},
        "assignees": 3,
        "day_part_weights": {"night": 0, "morning": 3, "noon": 10, "evening": 6},
        "desc": """For a long time you've been observing only light snowflakes, calmly
moving in the air, bringing thoughtfulness. But in some moment a
strange low distant sound attracts your attention. First you think
of an old airplane engine, still, after several seconds you understand
that it's an animal. In the same moment you see something dark on
the rails ahead, something blocking your path. Fastly taking the
binoculars to your eyes, you point it to the dark thing... And it
appears to be a deer! Huge, old and weak, most likely very ill,
lying right on the rails, crying to around. The animal better
be moved somewhere else! It'll be not very easy to deal with the
problem by your own, anyway three people should remain at the
Train to keep it safe. Who should you choose?""",
        "results": (
            {
                "score": range(0, 20),
                "desc": """{name1}, {name2} and {name3} stay at the Train. {name1}
and {name3} jumping off the locomotive, start to look around, while
{name2} enters the deckhouse. The lights are off! {name2} uppers {hisher2}
gun and silently moves to the lower level. The strong smell of diesel
flows around, the lights are also off here. {name2} takes a couple
more stepts in the switchers direction, when something jumps out
of the shadows and pushes {himher2} strong. Barely standing at {hisher2}
feet, {heshe2} sees a shadow of a human, slipping out of the door.
Hearing something, {name3} turns around and see a thin pale guy
running out of the door, jumping down to the ground. He has nothing
in his hands, so {name3} decides not to shoot. "He didn't get time
to grab anything." - {name2} says, appearing at the door. - "Let go."
{name2} getting Fear Of Dark""",
                "effects": {"char_2": {"add_trait": "Fear of dark"}},
            },
            {
                "score": range(20, 40),
                "desc": """{name1}, {name2} and {name3} stays near the Train by your
order. They promptly take positions around the locomotive, waiting for
your return. It didn't take long from you to move the ill deer away
from the rails, so you're returning fast. Jumping on the Train, you
enter the deckhouse and take a sit at your table... Something's
wrong. All of your stuff lie as it always does, but... something
changed. Opening the bottom drawer, you clearly see that some of
your money disappeared! You fastly exit the deckhouse and start to
gaze around. No one. Nothing. All of your fighter seem to be quiet
and calm. Someone entered the locomotive, took some of your money
and vanished! Converting the money, you see that not actually
much of money was stolen, 40$ probably. Anyway, it's no good!
You're losing 40$""",
                "effects": {"money": -40},
            },
            {
                "score": range(40, 60),
                "desc": """You're leaving {name1}, {name2} and {name3} to keep the
locomotive safe, and take a direction to the deer. Just several seconds
passed, and your sentinels hear some kind of a fuss in the deckhouse.
Opening the door inside, they see a girl about 18 years old, who
rummage through the things left on the table. She doesn't look thin,
or dirty, or anything like this. Good clothes, well face, clean hairs.
"Go away!" - {name3} uppers {hisher3} gun. Seeing that it's better not
to try tricking, the girl silently moves her hands up and takes a
direction to the exit. {name3} follows her outside to ensure she won't
do anything stupid, while {name1} and {name2} gazing at each other.
What was that? {name2} opens the aid kit: "I have an idea." Empty
syringe of painkillers lies inside with a blood drop on it. Addict!
You're losing -1 medicine box""",
                "effects": {"medicine_boxes": -1},
            },
            {
                "score": range(60, 80),
                "desc": """You're ordering {name1}, {name2} and {name3} to stay, while
you'll deal with the deer. For some time nothing promises issues, but
suddnely all three sentinels hear someone rummaging in the deckhouse.
Not poking around, they jump to the locomotive and fastly open the
door. A big armed thug is already waiting them, directing his pistol
to the entrance, but not shooting. Still, your fighters doesn't consider
this as an appropriate performance, so they lighting fast do
several shots at the man. With a wondering face he falls down on
the floor. {name1} silently moves closer to him and raises a bunch of
dollar banknotes. "Stealer!" - {heshe1} finalizes. Slapping the man's
pockets, {heshe1} raises even more money. "Well, who came with a
sword to us..." - {name2} says, getting closer to get rid of the body.
You're getting 70$""",
                "effects": {"money": 70},
            },
            {
                "score": range(80, 101),
                "desc": """You're taking your guns, but suddenly a kind of a grenade flies
into the open window. Grey tear gas starts to spread around fast with
a loud hiss. Pushing {name1} to the exit, you're grabing {name2}'s
shoulder with another hand and pull {himher2} with you. Exiting on
the air, you all upper your guns, trying to look through the tears.
For several seconds you don't see anything specific, but then you
catch your eyes on a couple of distant people. Without delays you
aim your gun and start to shoot at them, making them run away really
fast. Silence falls on the meadow, and you all take several minutes
to deal with tears. When your gaze clears completely, you take one
more careful look around, but no one seems to be in nearlands. Good!
The ambush was not successful. Time to ventilate the deckhouse.
Single character can get Deep Breath""",
                "effects": {"select_char": {"add_trait": "Deep breath"}},
            },
        ),
    },
    {  # 7
        "name": "Injured",
        "type": "Meet",
        "class_weights": {"soldier": 11, "anarchist": 20, "raider": 5},
        "assignees": 2,
        "day_part_weights": {"night": 3, "morning": 10, "noon": 7, "evening": 0},
        "desc": """You've noticed a big grey truck long ago. It has been riding in
parallel with you for about twenty miles, and now it started to
approach - the highway probably turned to the railways. The truck
seems to be in a good shape, and when it got closer you see that
it has several massive machine guns. Still, the people on the car
doesn't show any aggressive intentions, and the car stops on railway
to road crossroads in two hundred meters in front of you. Looks like
a dialog invitation, ha!? That makes sense to send a couple of people
to speak with those guys to get info about nearlands.""",
        "results": (
            {
                "score": range(0, 20),
                "desc": """You're sending {name1} and {name2} for a talk with the truck
party. Approaching quetly, your fighters smell something heavy.
A guy from the truck jumps to the ground: "Yo, folks!" - he smiles.
- "Have wounds?" - he examines both your messengers. - "We're taking
injured folks from all around, trying to get them to safety." He leads
{name1} and {name2} to behind of the truck and shows its inners.
There are at least fourty people covered with blood and dirty medical
bandages. So, that heavy cold metallic smell is their blood. {name2}
feels small needles started to run on {hisher2} back. "Skinheads
become more aggressive." - the man from the truck pronounces sadly.
- "We do our best..." Convincing him they are okay, your people
return back to you, trying to deal with the impact of the seen.
{name2} getting Nervousness""",
                "effects": {"char_2": {"add_trait": "Nervousness"}},
            },
            {
                "score": range(20, 40),
                "desc": """{name1} and {name2} taking a direction to the truck by
your order. Getting little bit closer, they see a dark inscription
on the car: "Injured". So, these guys are helping wounded people
around the place? Sounds good! {name1} and {name2} speed up their
steps, but in some moment people on the truck see something wrong
and start to shoot! Not giving them any chances, you all start
to fight back, and, feeling that gun power is on your side, the
truck spurts away really fast. What's happened? No one seems to
be wounded, and that's good, but, taking a look at the locomotive,
you see several big holes, made by the truck's machine guns.
Adjutant durability -50""",
                "effects": {"train": {"durability": -50}},
            },
            {
                "score": range(40, 60),
                "desc": """{name1} and {name2} start to move to the truck by your
command. While they are getting closer, a man from the truck jumps
down to the ground and meets them. "Hi, folks!" - he says loudly. -
"We're trying to get these injured people to the nearest city". Oh,
here is what the truck for! Your messengers follow the man, and he
shows them that there are at least thirty people in the car, all
covered in blood and white medical bandages. "Do you have seriously
wounded guys?" - he asks politely. "No, no, nothing we can't handle,
thanks." - {name1} answers fastly. - "That's nice to see someone
cares" - {heshe1} adds. "We all should do what we can!" - the man
pronounces loudly. - "Okay then, we better hurry!" - he smiles once
again to your messengers and moves back to the truck.""",
                "effects": {},
            },
            {
                "score": range(60, 80),
                "desc": """Your messengers, {name1} and {name2}, take direction to
the truck. A man jumps from the car down to the ground and starts
to move towards them. "Hey, folks!" - he says loudly. - "We're
helping wounded people all around the place. Don't any of you
need help?" {name1} and {name2} exchange glances, wondering the
man's kindness. "We're okay, thanks!" - {name1} answers. "Alright!"
- the man says something to his people, and one of them throws
a grey box to him. - "Take this at least!" - he holds out a box
to {name2}. Throwing one more glance to {name1}, {heshe2} takes
the gift, still wondering why the guy is so helpful. "Okay, let's
go!" - the man smiles to your messengers and climbs to the car.
You're getting 1 stimulator""",
                "effects": {"stimulators": 1},
            },
            {
                "score": range(80, 101),
                "desc": """{name1} and {name2} start to move to the truck. A man
jumps down from it to meet them. "Hey, folks!" - he greets them
loudly. - "If you have badly wounded guys, we can take them to
the nearest city." {name1} and {name2} think for a couple of
seconds. "Well, we're okay, I guess." - {name1} answers to the
man. "That's great news!" - he almost shouts. - "Maybe you need
one more gun? We have a potential recruit for you." - he whistles
to the truck, and someone in baggy clothes jumps down to the ground
and takes a direction to your people. "The wounds are healed, and
the element is eager to go to war! We're little bit tired already!"
"Well, that's something for our captain to decide" - {name1} answers.
One person can be recruited""",
                "effects": {"recruit": 60},
            },
        ),
    },
    {  # 8
        "name": "Old Church",
        "type": "Meet",
        "class_weights": {"soldier": 7, "anarchist": 13.3, "raider": 3},
        "assignees": 3,
        "day_part_weights": {"night": 0, "morning": 3, "noon": 10, "evening": 7},
        "desc": """The tall wooden spear that attracted your attention and made you
stop here appears to be a part of an old church. Its dark wooden
walls are ancient, white paint on the windows became grey, but you
see several people in black cassocks near it. They all are also old
- you can notice their long hoary beards. The people doesn't look
dangerous or even able to fight back in case of troubles, so you're
thinking about sending several of your teammates to speak with
locals. As an old dwellers they probably can tell you something
useful about the region you travelled into.""",
        "results": (
            {
                "score": range(0, 20),
                "desc": """You decide to send {name1}, {name2} and {name3} to negotiate
with monks. Seeing your people jumping off the Train, dwellers move
inside the church, keeping the door open however. Exchanging gazes,
your messengers approach carefully and hear a worship. Getting
closer to the door, {name3} takes a look inside, and in that
moment a hiss sounds in the air. In the next second scouts see
orange clouds in front of eyes, feel something heavy in their
heads, and cold sweat covers their skin. The Stench! Trying to
hold breath, without clear seeing of the way, they run back to the
Train... They find themselves on the half of a road between the
locomotive and the church, where the Stench didn't reach. "Let's
go, let's go, go!" - they shout, from a run jumping on the Train.
{name1}, {name2} and {name3} get -15 health and -25 energy""",
                "effects": {"assignees": {"health": -15, "energy": -25}},
            },
            {
                "score": range(20, 40),
                "desc": """You're choosing {name1}, {name2} and {name3} as a negotiation
party. Your people carefully get closer to the monks, and one of
the dwellers makes a step forward: "These sinners came from the
Hinnom Valley, they brought us the Stench of Hell itself!". In
the next moment a bunch of big rocks fly to your messengers.
Making several shots into the sky, {name1} commands others to get
back to the Train. Monks, seeing guns, run in different directions.
Retreating to you, your scouts climb to the Train fastly. It appears
{name3} got a rock right into {hisher1} head. The wound doesn't
seem to be very serious, but it's still very unpleasant.
{name3} getting -7 health and Motion Sickness""",
                "effects": {"char_3": {"health": -7, "add_trait": "Motion sickness"}},
            },
            {
                "score": range(40, 60),
                "desc": """{name1}, {name2} and {name3}, chosen as a talk group, jump
off the Train and go to the monks. The priests gather together,
looking at your people with a great attention. {name1} moves forward
and starts to speak with the Lord's people. The dwellers talk with
meek phrases, looking confused and embarrassed. It seems like they
don't have a lot of guests here... A couple of minutes of talking
ends with an invitation for a meal in the church. Exchanging gazes,
your people politely reject the proposition. Something not right with
these monks. They speak shy and meek, but their eyes are energetically
moving on your scouts, making small stops on the guns, knives
and sometimes on the Train standing in distance. It's better
not to trust these guys. Thus, your people return empty.""",
                "effects": {},
            },
            {
                "score": range(60, 80),
                "desc": """You choose {name1}, {name2} and {name3} as a negotiation
group. Your people take their guns and move to the monks. After
several minutes of talking one of the church inhabitants, a
young one, takes your messengers aside and speaks with them
tet-a-tet. It appears he want to buy a gun! "The elder part of
the commune thinks that God will keep us save, but, you know,
Lord will help those who will help themselves." - he explains,
stretching out a dollar banknote. Not thinking too long, {name2}
gives him {hisher2} excess pistol and takes money. Friendly
smiling, the priest hides the gun under cassock and says goodbye.
You're getting 50$""",
                "effects": {"money": 50},
            },
            {
                "score": range(80, 101),
                "desc": """You decide to send {name1}, {name2} and {name3} to talk
with the church beholders. Your people walk to the monks, and
the dwellers meet them with an open arms. It appears they heard
about your company fighting skinheads here and there, helping
people in the country. Two of the monks move into the church
and return back several minutes later with a basket of gifts!
Giving your people blesses and promising to pray for you, they
spend your messengers to the very Train. After all the goodbyes
said you open the basket and see cheese, wine, bread, flowers,
and, plus to this, a bunch of medicines and bandages! Exchanging
smiles, you and your teammates start to prepare a feast.
All of your teammates getting +30 energy
You're getting +1 medicine box""",
                "effects": {"all": {"energy": 30}, "medicine_boxes": 1},
            },
        ),
    },
    {  # 9
        "name": "Old Carriage",
        "type": "Meet",
        "class_weights": {"soldier": 20, "anarchist": 40, "raider": 9},
        "assignees": 1,
        "day_part_weights": {"night": 3, "morning": 0, "noon": 10, "evening": 7},
        "desc": """"On the east departure of Salzburg, on highway 158, big skirmish
happened today about 10:25 a.m.! Refugees, who got stuck in traffic,
started to threaten the people around to make them clear the road,
which caused a real fight..." Turning off the radio, you walk
outside the deck house. Fight for survival expands... A big dark
metal thing lying on the meadow between trees interrupts your heavy
thoughts. It seems to be an old railway carriage, moved out of the
way and abandoned. It wouldn't attract your attention, but you
also see a thin column of grey smoke, uppering from its inners.
Someone made a camp there?! It worth checking, maybe those
people need help or something.""",
        "results": (
            {
                "score": range(0, 20),
                "desc": """You call {name1} closer and show {himher1} the carriage. Squinting
eyes, {heshe1} nodds {hisher1} head and gears up for an outing. It
takes just several minutes for {himher1} to get to the carriage, and
you see how your messenger enters inside. In the next moment a din
thunders in the air. You're moving binoculars to your eyes, but
can't get what happened. Taking one more team mate, you run to
the carriage and, getting closer, see the problem. Heavy metal
door of the carriage slammed, prisoning {name1} inside. With common
efforts for about five minutes you finally release your trapped
messenger. Covered with spider web and dust, {heshe1} coughs, but
you don't see serious wounds. And the carriage itself appears
to be empty, you see only snow intensively melting to steam.
{name1} getting Fear Of Dark""",
                "effects": {"char_1": {"add_trait": "Fear of dark"}},
            },
            {
                "score": range(20, 40),
                "desc": """You decide {name1} will be an appropriate messengers this time.
Taking the gun, {heshe1} runs to the carriage, while you're observing
{hisher1} progress from the locomotive. {name1} slows down and approaches
the carriage quietly. You see {himher1} opening the sliding doors
and making a step inside. In that moment one of the doors breaks
down and falls right on your messenger. Pushing the metal thing away,
{name1} presses {hisher1} right hand to {hisher1} body. For several
seconds {heshe1} disappears inside the carriage, but then exits and
takes a direction to you. It seems like nothing interesting was there,
while {name1} got a minor right arm injury. Well, it could be worse.
{name1} getting -20 health""",
                "effects": {"char_1": {"health": -20}},
            },
            {
                "score": range(40, 60),
                "desc": """You call {name1} and explain {himher1} your thoughts. Nodding {hisher1}
head, {heshe1} runs to the carriage. You observe your messenger progress
from the Adjutant, seeing how {heshe1} carefully opens the carriage
doors and enters inside. Several minutes passes, and {name1} exits,
walking back to you. Getting closer, {heshe1} tells you the following:
"A refugees family made a camp there. Not sure how long they live in
that metal thing, but they are not going to leave. And they don't
want anything with us. They're not aggressive though, just not very
trustful. Can't blame them." Agreeing on that, you're giving a command
to warm up the Adjutant's engine. Let's continue the road.""",
                "effects": {},
            },
            {
                "score": range(60, 80),
                "desc": """You ask {name1} to get closer and explain {himher1} your thoughts.
Without arguments {heshe1} takes {hisher1} gear and walks to the
lying carriage. Carefully opening it, your messenger enters inside.
Time passes, three minutes, five, ten. At some moment you're going
to send more people to the carriage, to check if everythings is okay
with {name1}, but finally {heshe1} exits from the carriage. Getting
closer and climbing back on the Adjutant, {heshe1} explains: "There
are kids there! Not very young, but still kids. Asked me for some
ammo and gave me money. I've tried to reject, but they said they have
a lot of money. Not sure if it is true, still, I wasn't able to convince
them. Thus, we have some income." - {heshe1} puts a dollar paper on
the metal table. You give a command to warm up the engine.
You're getting 50$""",
                "effects": {"money": 50},
            },
            {
                "score": range(80, 101),
                "desc": """You're sending {name1} to take a closer look at the lying carriage.
Your teammate gears up and runs to the place, and then disappears
inside. After several seconds {heshe1} shows up and uppers {hisher1}
hand, making it clear that everything is alright. You take a seat and
start waiting. Not less than a half of hour passes, before {name1}
exits the carriage and runs back to you. "There are several refugees,
hiding in that carriage." - {heshe1} explains. - "Asked me to help them
with a water purifier. I'm not an expert, but dealt with the thing.
Still, they didn't have anything to repay except the kind words, so..."
You're accepting this - well, there's nothing wrong in helping
others. After all, your party is not in a critical state. You're
giving an order to start the Adjutant's engine.
{name1} getting Mechanic""",
                "effects": {"char_1": {"add_trait": "Mechanic"}},
            },
        ),
    },
]
