"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Outings scenarios and effects.
"""

OUTINGS = {
    "Plains": {
        "looting": (
            {
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
            {
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
go wrong it'll be a long way back for your teammates. So a couple of
people should be sent for a surprise case.""",
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
quick look, and turning back to Train. Obviously, there was nothing
useful in there. At all.""",
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
- {heshe1} pulls the zipper and stick his head into the stifling inners.
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
            {
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
your people. They are moving fast to Train, keeping their backside on
sights. But no one follows them. Coming closer {name1} explains to
you what happened back there: "Big dog, looks like it lives there.
And we found nothing". Your people are getting on Train in
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
        )
    }
}
