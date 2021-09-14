"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The main game scenario structure.
"""

SCENARIO = (
    {  # 1
        "intro": """Kenneth - the Adjutant mechanic approaches your table and sits to
the right of you. "Captain, we probably have a trouble." You're
uppering a spoon full of dry porridge to your mouth: "Yeah?!"
"Yeah. Come see me after you snack is over." He gets up and
leaves the deckhouse. Finishing the awfully tasteless portion,
you're walking to the lower level of the Adjutant. Before you
pronounce the first word, Kenneth rises his finger up, asking
you to stay silent and listen. You're concentrating on the noises...
"Hear that?" - the mechanic points to the left side of the room,
and you understand what he's trying to say. Some metal screeching
can be heard from the wall. "That's an axle box, something's
acting up." - Kenneth explains silently. - "We need to check
it, and it'll take some time." You're trying to remember how far
was the Stench frontier, when you last heard about it. "Our
options?" Looking at you, Kenneth calculates something in his
mind and then tells: "We need five hours long stop to deal with
the axle box." It's much. "Other options?" The mechanic seems
to be not very pleasant to say it, but he does: "We can try
to do it on move. But that's dangerous, and will require two
men - me here and someone on the other side of the locomotive.
The second guy can get injured I warn you. Anyway I think not
dealing with it can cause us troubles as well. Your call, Captain." """,
        "variants": {
            "Stop the Adjutant for a revision": {
                "desc": """You're making a decision to stop for, as planned, five hours. The
crew starts to work without delays. Dismantling the axle box,
you see that a couple of details do not fit each other, and
rub hard. Your people start to deal with the problem, leaded
by Kenneth. Seeing that they are okay to fix the trouble
without you, you return to the deckhouse and turn on radio.
"The Stench clouds were noticed in Stuttgart! On the south
of the city several people already found dead, others leaving
their homes, trying to get out of the city. Stay on this
station, we'll keep you posted!" Stuttgart. Looks like the
Stench frontier moves from south-east direction. It should
be considered while planning the further route... Four hours
passed, and the crew reports you that the axle box is good
to go. Calling everyone back on board, you're commanding to
continue the road in the same moment. Four hours is not five,
but it's still long, very long. Better keep your pace high now.

The Stench frontier came 20 miles closer to you,
but the Adjutant is in a good shape for now.

You're getting a Captain's diary page. Better read it while
on move not to lose distance from the Stench frontier.
Press J to open/close Captain's journal.""",
                "effects": (("do_stench_moves_effect", [20]),),
            },
            "Try to deal with the axle box on move": {
                "desc": """You're giving Kenneth command to choose one of your team mates
and try to deal with the axle box on move. You see that the
mechanic doesn't like your decision, but he still accepts
the order, promising to think who fits the task better.
You're returning back to the deckhouse, and some time later
see Kenneth taking one of the fighters with him to the
lower level of the Adjutant. For several long hours they
slip out of your radars... Exiting on the fresh air, you
incline above the railings and see a blood spot on one of
the wheels, blinking on every turnover. Without delays you
go to find the mechanic. Kenneth, seeing you concerned,
uppers his hands in the same moment: "It's okay, it's okay!
Small wound, but the axle box is fine now. Nothing serious!"
Making a deep breath, you nod your head, trying to calm
down. You knew the risks from the beginning, but it's still
about your people safety. It's good that the helper didn't
get serious wounds. You better find him or her later to
say your thanks.

One of your fighters getting -20 health

You're getting a Captain's diary page. Better read it while
on move not to lose distance from the Stench frontier.
Press J to open/close Captain's journal.""",
                "effects": (("do_characters_effect", [{"health": -20}, True]),),
            },
            "Ignore the problem": {
                "desc": """It's better not to stop for such long period. Asking Kenneth
to wait for some time, you return back to the deckhouse. It
is better to double check. The Stench frontier is far back
for now, but three hours later... Looking at the map, you
understand that you can't afford even three hours. Too risky,
in these days it's better to keep some spare time. Returning
back to Kenneth, you tell him to ignore the noises for now.
He doesn't like your decision very much, you can see it on
his face, but your common past outweighs everything. You
helped him and his family more times than you both can count,
so he's not going to argue with you...

Some time later you'll understand that the problem was not
one of those to be ignored. The axle box will be damaged.

The Adjutant loses 50 Durability

You're getting a Captain's diary page. Better read it while
on move not to lose distance from the Stench frontier.
Press J to open/close Captain's journal.""",
                "effects": (("do_locomotive_damage", [50]),),
            },
        },
    },
    {  # 2
        "intro": """Taking a closer look at the bunch of people walking through the
meadow, you understand that there are mostly children. Weird!
Asking a couple of teammates to follow you, you get closer
to the crowd, seeing a woman moving towards your party. In
a few words she tells that they are workers and children
from an orphan shelter. Understanding that the Stench moves
fast to the place, and the governors are too busy saving
themselves, adults, who worked there, gathered all the
children and decided to move to Silewer on foot. Looking at
pale and tired kids, you silently think that it was really
tough idea. But probably the decision saved their lives...
Complaining about walking for six hours without a stop, the
woman asks you to help them build a field camp. You understand
that it'll take a lot of time, as there are about sixty
children. On the other hand, it doesn't look right to just
leave them here, in the foreign country, tired and
shelterless. Maybe there is some time to help them a little?""",
        "variants": {
            "Help them to build a camp": {
                "desc": """Feeling some qualm inside, you give your people order to help
the children. Losing time is not okay... Still, twenty minutes
later, seeing your people and children smiling while setting
up big tents, igniting bonfires and boiling pottage in big
cauldrons, you forget these heavy thoughts. This small break
will be useful for the crew as well... It takes you about two
hours to finish preparing the camp. Getting a lot of thanks
from the children and their teachers, you gather again on the
Adjutant. Everyone seems to be enlivened, still, the road calls.
Giving an order to start engine, you approach a couple of your
teammates, who are viewing some kind of an article on a
smartphone. "Hey, Captain, you need to see this! Some of those
children visited kinda scientist summit some time ago and took
an interview there. The woman speaks about interesting things."
Telling them that you're going to take a closer look at the
article later, you go to the deckhouse to plan the route,
considering the recent delay.

The Stench frontier came 20 miles closer to you

A note added into Captain's journal. You can read it
on move not to stay long at the same place, losing
distance from the Stench frontier.""",
                "effects": (
                    ("do_build_camp_effect", []),
                    ("do_stench_moves_effect", [20]),
                ),
            },
            "Agree in words, but steal from them": {
                "desc": """Calling the crew to speak aside, you're trying to convince
them to use an ability to replenish resources. "The situation
is getting tougher day after day, it's becoming about us or
them." Your teammates lower their eyes. Everybody know that
sooner or later it'll come to this, still, no one wants to take
responsibility. "It's hard to admit, but those children are not
going to make it. They are not fighters nor survivors. The first
meet with skinheads, and..." The crew continue to keep silence,
bit you feel them accepting the situation, so you're giving an
order: "Build the camp hastily, and take useful stuff in case you
see it!" Your teammates, avoiding to look at each other, go out
of the deckhouse... About an hour and half passed, and all of
your people gather together on the Adjutant. They still doesn't
want to look at each other, but they put an aid kit and an energy
drink on the table. "Okay, let's move on!" - you command.

Some time later you find a paper on your table, which looks like
an interview log. It appears those children visited a kind of a
scientist summit recently and had a word with one of scientists.
No ideas why someone left the paper for you, but it worth reading.

You're getting 1 medicine and 1 stimulator
Soon people of Silewer will know that you've stolen from kids.
This will be a bad example of what foreigners are like and will
bring more people under the skinhead banners.

A note added into Captain's journal. You can read it
on move not to stay long at the same place, losing
distance from the Stench frontier.""",
                "effects": (
                    ("do_enemy_inc_effect", []),
                    ("do_plus_resource", ["medicine_boxes", 1]),
                    ("do_plus_resource", ["stimulators", 1]),
                ),
            },
            "Don't help them and continue the road": {
                "desc": """You go back to the deckhouse and negotiate with the crew. It
appears most of them would like to stop and help orphans, but
all understand that it'll take at least several hours. Clouds
of the Stench will not let you wait, so it makes sense to move
faster. People know nothing about the cataclysm behavior, in
theory it can accelerate or appear somewhere far from the
supposed source in Germany. Overthinking it again, again and
again, you decide to ignore the teachers plea. The crew don't
like the decision very much, but everyone mind the situation.
A hard silence forms in the air. No one wants to go there and
say those orphans that you're going to leave. "So, what?" - you
ask quietly. - "Should we continue the road without the last
word? What's the point in it?" Your teammates lower their
eyes and nod their heads. Taking this as an answer, you give
a command to go...

Some time later you see a paper on your table. Running through
it with your eyes, you find out it's an interview log. Those
orphans visited kind of a scientist summit some time ago and
took an interview from one of the scientists. Most likely one
of your people got it from the children somehow. No thoughts
why it was left on your table, but it should be read.

A note added into Captain's journal. You can read it
on move not to stay long at the same place, losing
distance from the Stench frontier.""",
                "effects": (("do_no_effect", []),),
            },
        },
    },
    {  # 3
        "intro": """Looking at an old house, standing in about 300 meters aside of
the railway, you see some kind of a fuss there. The hut is
really old, the walls are crumbled here and there, the old
dark wooden roof holds on a promise, but through small windows
you can discern several people moving actively inside. You
also hear some noise, even screams sometimes. That's worth
checking the place... You take a couple of your teammates and
get closer to the building. It appears a police jeep is standing
from the other side of the hut. Entering the house, you see a
couple of men in uniform, threatening an old pair and a young
girl, most likely their daughter. Interrupted and surprised, the
police officers look at you, trying to understand who are you.
Seeing your guns, they become very friendly: "Hey, folks!
Nothing interesting here, we're just helping this family with
something." Throwing a gaze at the scared people, you realise
it's a lie. "Maybe we can bet a deal and live on happy?" - one
of the officers does a step to you, lingering a wallet from his
pocket. No doubts, they are caught doing something bad, two
officers threatening people in backcountry - witnesses can turn
it dangerous for them. The law didn't collapse completely yet.""",
        "variants": {
            "Take the bribe and go away": {
                "desc": """Nodding your head to the door, you're commanding your people
to leave the house. It's not your fight, not your people, not
your business. The threatened family keeps silence, but you
can feel with your skin that, seeing your gesture, they've
lost the last hope for a better end. As if emptiness filled
the part of the room, where they're sitting. Taking money
from the officer, you exit the hut without a word... While
walking back to the Adjutant, you're all trying to hear anything
from the house side, but nothing happens. Turning your head
back, you see one of the men standing near the door, looking
at your crew. Seems like they are scared by themselves and
doesn't believe you'll just leave. Still, you're leaving.
Soon this will be happening everywhere - those, who has
power and strength, will be using it to survive, destroying
others if needed. And it will be needed. You can't save
all the others anyway, but you can take care about your crew.

You're getting $100

You've got one more diary page in Captain's
journal. Better read it on move.""",
                "effects": (("do_get_money", [100]),),
            },
            "Kill the bastards and free the family": {
                "desc": """Lighting fast overthinking the situation, you upper your gun
and shoot both policemen. With the same surprised faces they
loudly fall to the floor. Taking away the gun, you do a step
towards the threatened people, but they all upper their hands
in the same moment. "Please, just leave us!" - the old man says
with a trembling voice. Seeing they became even more frightened
than before you killed the intruders, you realise that it
wasn't a good idea to do it all in front of them... Everyone
in the room seems to be little bit lost. It probably will be
better to just leave. Still, you decide to give an order to
your people to pull both bodies out of the hut and drop them
in some distance. Without arguments, they take both dead
policemen and exit the house. After a few seconds long pause
you throwing the last gaze at the frightened family: "Sorry...
Sorry for the mess." Not getting any sound from them, you're
leaving the hut.

You've got one more diary page in Captain's
journal. Better read it on move.""",
                "effects": (("do_no_effect", []),),
            },
            "Use your superiority and intimidate them": {
                "desc": """You see clearly that all the points are on your side. These
two men are weekly armed, they are policemen, and they were
caught on very bad dids. Every part of the situation is
against them. Tinkering the gun in your hands, you say
overbearingly: "You two better leave this family and forget
the way to this house!" Smiles disappear from their faces
in the same moment. Throwing gazes to each other, they seem
to be confused greatly. "We all will forget what happened
here, you only need to leave" - you add. - "But if you have
any counter arguments... Well..." - you move the gun again.
"Okay!" - one of the policemen uppers his hands. The second
one follows his gesture in the next second. "We'll go. Let's
just... Just forget about what happened here." - the officer
seems to be even ashamed, and this fact makes you think they'll
not return here - maybe they even understood what they were
just doing... When the men left, and their car engine silenced
somewhere in distance, the young girl stands up: "Thank you!
Thank you!" - she seems to be too touched, and you all hear
her gratitude for several minutes. In return she proposes your
crew a medical examination. Yeah, she's a doctor! Feeling the
very lucky coincidence here, you command your people to use
the opportunity.

All people in the crew getting +20 Health

You've got one more diary page in Captain's
journal. Better read it on move.""",
                "effects": (("do_characters_effect", [{"health": 20}, False]),),
            },
        },
    },
    {  # 4
        "intro": """From a very far distance you can discern that near the small
motel a long line of cars jamms. You can even see a long
string of people standing in front of the entrance. Looks
like a lot of Silewer newcomers want to rent a room here.
Sending your people to try to get inside the building, you
caught your eyes on two banches of refugees arguing hard.
Getting closer to them, you can hear that they are brawling
because of the last place in the building. When they see
you, however, they become silent, gazing at your guns. In
a couple of moments you take a place of judge here, you
see both sides looking at you with hopes to get your help.
Observing them, you get it that one of them is a man with
sick boy, about eight years old, most likely his son. The
lad doesn't look good, his face is pale, dark rounds mark
his eyes and skin is covered with sweat. But on the other
side of the conflict you see a pregnant woman, skinny and
tired. Both the father and the woman expect your judgment
somewhy, probably because others are too busy by
themselves to think about people around... Or maybe it's
just because of guns... Anyway the decision is yours -
there is only one place left in the motel and someone will
have to sleep in the car here.""",
        "variants": {
            "The pregnant woman should rest": {
                "desc": """Thinking about the situation, you tend to think that
the woman is the one to take the last place in the motel.
The man with the sick boy throws something on the ground
and, grabbing his son, goes away. The woman, who still
seem to be scared, thanks you greatly - you can even see
tears in her eyes. Seeing your people returning back from
the motel, you say her goodbye and join the crew. According
their words, the place is filled to the very top, some
unfamiliar people even rent rooms together. Plus to the
things you already understood by yourself, your team mates
give you a log paper - one of them heard how the motel
dwellers were conversing about the same scientist those
orphans were interviewing. She was here not long ago!
That's something should be read.

Some time passed, you're going to give a command to start
an engine, but suddenly you see the man, who was trying to
get the last place in the motel. The one you forced to go
- he walks from the Adjutant back in the motel direction.
What does it mean? You ask the crew to check if everything
is okay on the locomotive, and it appears the man ignited
it! You deal with fire fast, but still the Adjutant gets
some damage.

The Adjutant loses 70 Durability""",
                "effects": (("do_locomotive_damage", [70]),),
            },
            "The man with the sick son should rest": {
                "desc": """Overthinking the conflict, you decide that the man with
the sick boy should rest in the motel. The woman seems to
be tired, but not hard ill. Saying something silently, most
likely damnations, she leaves the place. The man holds
out his hand: "Thank you!" - he lowers his eyes back to
son: "Jerry!" The boy slowly gets what his father is asking:
"Thanks!" - he pronounces with a weak voice. Left them,
you join your crew. They tell you that the motel is filled
to the very top, but it's something you already got by
yourself. In addition, they give you a note - they heard
a conversation between two motel dwellers, who saw the same
scientist woman those orphans were interviewing. And they
said that she's one of those who responsible for cataclysms
like the Stench. Interesting! The note made by your people
definitely should be read.

You're doing a short technical review of the Adjutant and
then start the engine to continue the road.

Soon all the Silewer will know that armed foreigners forced
a pregnant woman to leave the motel, where she was going to
rest after long road. This will bring more people into the
skinhead bands.""",
                "effects": (("do_enemy_inc_effect", []),),
            },
            "Force them both out and take their place": {
                "desc": """The last room in the motel... Maybe it's better to keep
it for your crew? A couple of hours in not moving place
and shower would be good. Looking straight at both the
man and the pregnant woman, you say in a cold voice: "Me
and my crew will take the room." Your visavis stagger back,
surprised greatly by the turn. Several seconds they look
at each other, and then simultaneously turn around and go
away. You join your crew and rent the room... The short rest
goes okay, one of your team mates even give you a paper, on
which he noted a conversation between two motel dwellers,
who were speaking about that scientist woman, interviewed
by orphans you met earlier, blaming her in cataclysms like
the Stench. Interesting!

In some moment you understand that a kind of a noise
increases fast in the motel. Taking your guns, you all
get out of the room and get into a fight! It takes about
ten minutes for you to exit the building. Without clear
understanding what happened - are refugees, who didn't
manage to get a room, decided to attack the building? -
you return back to the Adjutant. No one got serious
wounds, still, there are several small injuries. Not
the best stop!

All people in the crew getting -20 health""",
                "effects": (("do_characters_effect", [{"health": -20}]),),
            },
        },
    },
    {  # 5
        "intro": """Seeing a couple of cars and a crowd, you're giving an order
to stop the Adjutant and see what happened. Approaching, you
understand that a fight just finished here - a big bus is full of
bullet holes, and a black jeep lies on its side, also shot bad.

A man walks to you and tells: "Some bandits were following a
column of black jeeps. Good they didn't decide to stop for us,
still, several gun bursts hit our bus." Looking at dense smoke
rising from it, you get it's not gonna ride. The man notices
your gaze and asks for help in repair. You start weighing,
while your collocutor adds: "We searched the jeep for tools -
poor bastards both caught bullets. Unfortunately, there is
nothing useful, only tons of paper, some high science mumbo
jumbo and gas masks." Listening to the guy more carefully,
you start to suspect you already know who was in those
cars... Helga Wagner! Looks like you're almost following her.
Interesting. It's worth checking the jeep - last pieces of
info about the Wahrsager project sounded intriguingly.

The only thing left to decide is of helping these people.
Throwing one more gaze at the bus, you see a lot of bags
on the car top, german car number - they are refugees.
If those bandits they met were skinheads, shooting at
the bus wasn't occasional. The scum can return here
when they'll deal with Helga's group...""",
        "variants": {
            "Help them to repair the bus": {
                "desc": """Overthinking the situation carefully, you decide to
help these people. Your crew brings tools from the
Adjutant and starts to reanimate the car. Taking part in
it, you're studying the refugees. Confused and nervous,
they seem frustrated hard. Usually, refugees coming TO
Europe, but the Stench seems to be turning everyone into
the opposite direction. Europe! The place of comfort,
order and civilization became the most dangerous place
in the World. Where to go now? Who'll welcome us?
Countries, which are not able to help themselves? Most
of their citizens would like to live in Europe, but it's
unlikely they want us to come to them and take their
places. Of course, they don't want, especially now, when
number of places reduces really fast, and no one know
if it'll stop one day...

A couple of hours passed, and the bus engine finally
starts to roar, gathered from, literally, pieces. People
give you sluggish thanks, you see they are still too
shocked after getting under a machine gun fire. Anyway,
they at least can now move forward.

The Stench frontier came 20 miles closer to you.
In the black jeep your people found a piece of Helga's
diary. It's added to your journal, worth reading.""",
                "effects": (("do_stench_moves_effect", [20]),),
            },
            "Give them tools from the Adjutant": {
                "desc": """Seeing you doubt on your decision, the man proposes:
"Maybe you can at least bring us some tools? Money is
critically needed now, but we'll pay you!" Don't do a
stop, help them and get some money - sounds good. You're
commanding the crew to give the people stuff, which'll
help to repair the shot bus, while the man gathers
some money from his passengers. Approaching you back,
he gives you $80 totally. "Not much actually, sorry."
- he pronounces quietly. - "Those people are still
shocked by the skirmish, that's not what we expected.
Not in the second day of the road at least!" Nodding
your head, you think that it's weakly said. Usually
people go TO Europe, not out of it. But now the spot
of comfort, civilization and order became the most
dangerous place in the whole World. A lot of directions
changed to opposite. Who'll welcome new refugees from
Europe? People, who wanted to refuge to Europe? Looking
at the bus covered with bullet holes, you think it's
unlikely. What happens in Silewer is just a start,
it'll become more worse, if the Stench will grow.

You're getting $80.
Soon you'll understand that you gave too many things to
those people, so you're not able to fix problems on the
locomotive. The Adjutant getting -70 Durability.

In the black jeep your people found a piece of Helga's
diary. It's added to your journal, worth reading.""",
                "effects": (("do_locomotive_damage", [70]), ("do_get_money", [80])),
            },
            "Don't help them": {
                "desc": """Overthinking the situation, you decide it's too risky to
do another stop. The bus looks pretty bad - it'll take
hours to reanimate it. You don't have hours.

Saying goodbye to the man, you turn back to the Adjutant,
by the way looking at the bus passengers. Refugees.
Yeah, it's time people come out of Europe instead of
moving into it, who'd knew. The spot of order,
civilization and comfort became the most dangerous place
in the World. An interesting question is: who will
welcome new refugees? Looks like the answer to this
is right in front of your eyes - the bus shotted from
a machine gun. And this can be only a beginning! No one
stopped the Stench yet, no one have any ideas about it
actually. If it'll continue to grow, more people will
left their homes and will go to the neighbour countries
and even further. Some will not stop in face of any
counteraction, because it's no longer about simply
comfort and wealth, it's became about survival...

Climbing on the Adjutant, you give an order for your
crew to search the black jeep for anything useful and
continue the road. Survival - so, let's not waste time!

In the black jeep your people found a piece of Helga's
diary. It's added to your journal, worth reading.""",
                "effects": (("do_no_effect", []),),
            },
        },
    },
    {  # 6
        "intro": """Running a rag across the floor, you're working out your turn
to cleanup the Adjutant. Tidiness is important - so many days
in the same cold and coarse locomotive rises chances of
sickness and pests emergence...

At some moment Daren, the Adjutant machinist, approaches you.
You see he has something to tell you, but he can't find the
proper words. "Come on, Daren, birth it." - you say, trying to
make things faster. "Well... We've a problem. It's big.
Precisely, we don't have food." Stopping to run the rag, you
straighten your back: "How so?!" "Well, everyone is waiting
you." - he answers and disappears in the doorway. Thinking a
couple of seconds what it should mean, you decide to hurry
up to the crew - if EVERYONE is waiting, it's serious.

Entering the back room, you see all of your people standing
in a circle. Everyone seems to be concerned, but you don't
find any aggression in the room, fortunately. "Well, Captain,
here we are." - Kenneth starts the talk. - "Our food supplies
are running out faster than we thought. We need to speak
about limits, otherwise, we'll soon start to starve." Rubbing
wet hands, you're trying to concentrate on the new problem.
In current situation everybody should be energetic and
healthy, as there are a lot of maintenance questions and
the need to fight. But if it's impossible, maybe it's worth
choosing who should have a priority in food questions?!""",
        "variants": {
            "Fighters will have food priority": {
                "desc": """Keeping silence for about two minutes, you come to
a decision that fighters, those who protect the Adjutant
from skinheads and who search resources on outings,
should eat enough. If they'll not be able to fight back,
you all will become victims of savages people turning
into. As for the Adjutant mechanic and machinist, well,
their work is less nervous and doesn't require that
big efforts and concentration.

Pronouncing your decision to the crew, you see they are
not very pleased with it. Most likely, they are ready to
starve together, instead of choosing special ones...
Still, these days require tough turns and tactical
thinking. Fortunately, Kenneth and Daren doesn't seem to
be offended that their ration was reduced. They are not
young, both seen a lot in their lives, they understand
and can handle it. Good. Not that good, of course, but
at least you don't need to think about riot in the crew.

Finishing the talk, you return back to your cleaning duty.

Some time later you'll find out that reducing mechanic's
ration was not the best solution, because malnutrition
lowered his competence, and the locomotive suffered.
The Adjutant getting -80 Durability.

You're getting a new diary page. Check the Journal.""",
                "effects": (("do_locomotive_damage", [80]),),
            },
            "Adjutant maintainers will have priority": {
                "desc": """You're keeping silence for several minutes, weighing
all the points. Fighters are needed, but you have enough
ammunition - it's the main part of the defence. But if
the locomotive engine will stop... In this case you all,
without counter arguments, will die really soon. Keeping
the pace is important, more important right now than
killing those savages.

With this in mind, you're pronouncing your thoughts to
the crew. Kenneth and Daren seems to be not very
pleasant with your solution - they both are not young,
they've seen a lot and can handle some starvation. Your
order little bit offends their pride. Still, order is
yours, and you believe the mechanic and the machinist
should been in the best condition that is possible in
the current situation.

Finishing the talk, you return to your cleaning duty.

Some time later it'll become obvious that fighters
tired much faster with this malnutrition, and their
productivity significantly reduced.

All the fighters getting -40 energy.

You're getting one more diary page. Check the Journal.""",
                "effects": (("do_characters_effect", [{"energy": -40}]),),
            },
            "Limit food for all": {
                "desc": """Taking a couple of minutes to think about the situation,
you decide it's not the best idea to make a part of the
crew somewhat special. Everyone is important, everyone
here do something for the whole company. If food supplies
are not enough, it'll be better to reduce ration equally
for all, no matter their duties.

Sounding your solution, you see that everyone in the room
is completely okay with it. Good, the team spirit is still
here, and the food crisis will be dealt with by common
and equal limitation.

Calculating the new ration with others, you understand
the limitation will be actually small - spreaded to every
person, it became not very significant for separately
taken member of the crew. With this, you all approve
the decision and return to your duties.

Ration limitation results:
All the characters getting -10 energy and the Adjutant
getting -20 Durability.

You're getting one more diary page. Check the Journal.""",
                "effects": (
                    ("do_characters_effect", [{"energy": -10}]),
                    ("do_locomotive_damage", [20]),
                ),
            },
        },
    },
)
