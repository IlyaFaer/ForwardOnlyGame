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
                "class_weights": {"soldier": 16.6, "raider": 10},
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
You're getting +90$ and fuel for 50 miles
{name1} getting - 15 health""",
                        "effects": {"money": 90, "char_1": {"health": -15}},
                    },
                ),
            },
            {  # 2
                "name": "Big Tent",
                "type": "Enemy Camp",
                "class_weights": {"soldier": 50, "raider": 25},
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
                "class_weights": {"soldier": 25, "raider": 15},
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
gang in the jeep approaching fast are starting to shoot, and you're
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
                "class_weights": {"soldier": 25, "raider": 16},
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
                "class_weights": {"soldier": 16.5, "raider": 11},
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
the car for several seconds and walk out together, holding a big canister.
Lifting it onto the Train, {name2} puts {hisher2} hand in {hisher2} pocket and
gets out a bunch of dollar papers. "Plus to the fuel" - {heshe2} smiles.
You're getting fuel for 50 miles and 60$""",
                        "effects": {"money": 60},
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
        ),
        "looting": (
            {  # 1
                "name": "Abandoned Car",
                "type": "Looting",
                "class_weights": {"soldier": 25, "raider": 50},
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
red canister in {hisher1} hands, and uppering your hand with a like-finger,
as there is a diesel fuel for 40 more miles.""",
                        "effects": {},
                    },
                ),
            },
            {  # 2
                "name": "Meadow Tent",
                "type": "Looting",
                "class_weights": {"soldier": 15, "raider": 25},
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
{heshe2} shows up with a big canister. Smiling both {name1} and {name2}
are returning to Train with this burden.
You're getting diesel fuel for 35 more miles.""",
                        "effects": {},
                    },
                ),
            },
            {  # 3
                "name": "Old Hut",
                "type": "Looting",
                "class_weights": {"soldier": 11, "raider": 16.5},
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
                "class_weights": {"soldier": 11, "raider": 16.5},
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
strange sounds and shouts. Moving closer to the building they decide
to take a look through the window. {name2} sets a knee to give a lift
to {name3}, while {name1} stands near on a watch for troubles, as in
this noise they hear human voices, and they are many. Lifting up {name3}
takes a look inside the monastery, and sees at least forty people
in there. Dirty, unkempt and completely crazy, they are ripping to shreds
several animals and eating them raw, all covered in blood. Seems like kind
of cultists are celebrating the End of the World. {name3} moves down and
silently explains what {heshe3} saw. Deciding not to disturb this mad
gathering your people returning back to the Train.""",
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
                        "effects": {"all": {"health": 20}},
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
                "name": "Wrecked truck",
                "type": "Looting",
                "class_weights": {"soldier": 16, "raider": 25},
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
                        "effects": {},
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
        ),
    }
}
