"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Captain's journal GUI.
"""
from direct.gui.DirectGui import (
    DGG,
    DirectButton,
    DirectFrame,
    DirectLabel,
    DirectScrolledFrame,
)
from panda3d.core import TextNode, TransparencyAttrib
from gui.widgets import RUST_COL, SILVER_COL

JOURNAL_PAGES = (
    (
        "diary",
        """Never wrote diaries earlier, but now I feel
that I need to put all of my thoughts
down on paper and try to look at what
happened recently, see a bigger picture...

About a month ago social networks gave
birth to a new flow of videos. People were
filming streets, talking about some kind
of orange mist. But there was no mist!
What they were trying to film was only
buildings, cars, sidewalks, and crystal
clear air. Like they were hallucinating.

It all looked as a new stupid joke from
those internet guys, but in some moment
they started to find bodies... More and
more: people were dying right on a street,
but no one was able to say why! Here
someone noticed: bodies appearing in
regions where that orange mist was spotted.

As it usually happens, government first
tried to hide the adversities scale. They
started to close city blocks, speak of
stupid explanations, while in Germany,
Switzerland, Netherlands more and more
bodies were appearing, more and more
orange mist reports were happening.

Finally, several police officers, seeing
that the disaster is gaining momentum,
decided to whistleblow. Photos they
posted publicly were showing tens of dead
bodies on streets, and several documents,
where chemical specialists were summaring
up that the orange mist, called by them
as "The Stench", selectively kills people,
no matter how good is their isolation
or air filtering...

This action caused panic to stroke most
of the Europe countries, and in this
moment I reilized I should do something.""",
    ),
    (
        "note",
        """Interview protocol from 2021-06-23, Zurich,
56th World Scientist Summit.
Interviewer: Emily Schlosser
Interviewee: doctor Helga Wagner,
leading system engineer of Wahrsager
project team.

- E: Helga, could you explain our
subscribers in simple words what the
Wahrsager project actually is?
- H: Before talking about the project
itself we should remember determinism:
the methodology which proclaims that
every event in the world has particular
causes. This idea actually means that
our past directs our future. With this
in mind our group of scientist tried to
find a way to take a look at our past,
see what was actually happening there,
measure previous events and, probably,
we hope, use this information to predict
our future! That's how the Wahrsager
project idea was created.

- E: What you're talking about sounds
pretty much like a time machine!
- H: Ya! But let's mention this machine
doesn't make passages into another time,
it only gives us an ability to take a
look at it, do a detailed snapshot, which
can be analyzed. Like a photo. The main
point here is accuracy - our world consists
of immeasurably number of events, which
influence each other. We need Laplace's
Demon to get results, as without high
accuracy our data will be giving pretty
unreliable predictions.

- E: Sounds incredible! But it seems you
need the best equipment and experts.
- H: Sure, our team consists of the
highest level professionals, and it's
a great honor for me to work with these
brilliant people! As for equipment, our
government provides us everything we
needed since we've run the very first
presentation.

- E: Could you tell us how it was?
- H: Right now we proceeded further than
that, but the first presentation included
only a chamber with a chemical substance
and equipment, which was able to show the
state of this substance 48 hours back in
the past...

On this question our interview came to
its end, as doctor Wagner was called by
her colleagues to take part in some kind
of an urgent online meeting.""",
    ),
    (
        "diary",
        """When it became obvious that the Stench
adversity is real, and it's not going to
stop in the near future, I decided to close
my company. Those who worked for me -
we were always like a family. I don't have
another, so it was hard to say goodbye to
everyone... Still, we all made a decision
to leave the city as soon as possible.
The first Stench reports were made in
Germany and Switzerland, most likely on
the west, so we had an approximate
direction - considering that the mist is
going to spread in circle.

As we were little bit slowly, we really got
stuck! Airplanes, which've taken some
people, flew away and refused to return.
No single airplane left in the whole
country! As for the cars, well, it was even
worse - every road on the west of the city
was clogged up in miles, MILES!
Everybody was trying to leave the place.

Here one of my friends, a machinist
called me. He was in search of people,
who are brave or desperate enough to help
him to hijack the locomotive he was
working on during the last several years.
He know me as a daredevil, and decided
to call me first. I liked his idea and
made a proposition to my workers. Some
of them have families, so they refused
to take part in this risky operation,
but three of them and Kenneth, my old
friend mechanic, agreed.

Daren, the machinist, who proposed all
of it, told us about the Adjutant -
tough locomotive he was driving, the
fast and powerful machine, which is old,
but very reliable transport. He said he
knows a forsaken closed railway, which
condition is still quite good and which
can lead us out of the city. On that we
all made a decision.""",
    ),
    (
        "note",
        """Following is what I've heard from one of
the motel dwellers, who was in a very
dissatisfied manner telling a story about
a strange woman to his friend.

According to the source of information,
yesterday in the morning he met a woman
with a very strange thing on her neck,
looking pretty much like a high-tech gas
mask. She had several metal boxes and
a bunch of helpers, all seem to be a part
of university or a science group.

The woman have been talking a lot with
someone on the other end of the phone.
He said she was reporting. According to
what our man heard, they were working on
some kind of a machine, which attracted
government attention pretty strong.

It's able to make a window into the past
(Wahrsager project, no doubts). They
wanted to use it to check if people are
lying about things already happened, and
for espionage - getting info about what
happened some time ago, but didn't yet
caused any consequences. As the machine
shows how it was actually been, without
embellishing, hiding or concealing, just an
objectively truth, it all sound really smart.
Let's say, a spy was rooted a couple of
days ago into your organization; with this
machine you can see the past, the period
when he was recruited and instructed.
You'll detect danger before the guy will
actually get hands on something valuable.
You can actually track anyone! With some
delay, yes, but still...

The woman also told about some of their
early experiments. They created portable
version of the machine and tried to
look into 1928 to investigate a murder
of a 10 years old girl named Grace.
They've got good results and were able
to track the whole horrors of the crime
from the very start to the last second.

An interesting thing is that on images
scientists noticed color deformation of
some fluids. They said that it has too
much of red and green. Which means they
were more ORANGE than they should. (I
think here the guy gave free rein to his
imagination, and there was nothing about
it in the scientist's conversation).

To the end of the story the man cursed
scientists, saying that it's they who
start adversities like the Stench,
Bhopal Disaster, Fukushima-1 Nuclear
Power Plant Accident, Minamata Disease
and others, and one day they will kill
us all. On that the interesting part
of the conversation ends.""",
    ),
)


class Journal:
    """Captain's journal GUI object."""

    def __init__(self):
        self._is_shown = False
        self._main_fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.37, 0.38, -0.6, 0.6),
            state=DGG.NORMAL,
            pos=(0.37, 0, -1),
            frameTexture="gui/tex/paper1.png",
        )
        self._main_fr.setTransparency(TransparencyAttrib.MAlpha)
        self._main_fr.hide()

        self._fr = DirectScrolledFrame(
            parent=self._main_fr,
            frameSize=(-0.35, 0.3, -0.46, 0.5),
            frameColor=(0, 0, 0, 0),
            canvasSize=(-0.31, 0.3, -1, 1.5),
            state=DGG.NORMAL,
            pos=(0, 0, -0.1),
            verticalScroll_frameSize=(-0.003, 0.003, -0.5, 0.5),
            verticalScroll_frameColor=(0.46, 0.41, 0.37, 1),
            verticalScroll_thumb_frameColor=(0.31, 0.26, 0.22, 1),
            verticalScroll_incButton_relief=None,
            verticalScroll_decButton_relief=None,
            horizontalScroll_relief=None,
            horizontalScroll_thumb_relief=None,
            horizontalScroll_incButton_relief=None,
            horizontalScroll_decButton_relief=None,
        )
        DirectLabel(  # Journal
            parent=self._main_fr,
            text=base.labels.JOURNAL[0],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            text_scale=0.045,
            text_bg=(0, 0, 0, 0),
            frameSize=(0.1, 0.1, 0.1, 0.1),
            pos=(-0.34, 0, 0.52),
            text_align=TextNode.ALeft,
        )
        DirectLabel(
            parent=self._main_fr,
            text=base.labels.JOURNAL[1],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            text_scale=0.03,
            text_bg=(0, 0, 0, 0),
            frameSize=(0.1, 0.1, 0.1, 0.1),
            pos=(-0.34, 0, 0.47),
            text_align=TextNode.ALeft,
        )
        DirectLabel(
            parent=self._main_fr,
            text=base.labels.JOURNAL[2],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            text_scale=0.03,
            text_bg=(0, 0, 0, 0),
            frameSize=(0.1, 0.1, 0.1, 0.1),
            pos=(-0.34, 0, 0.44),
            text_align=TextNode.ALeft,
        )
        self._page_text = DirectLabel(
            parent=self._fr.getCanvas(),
            text="",
            text_scale=0.03,
            text_font=base.main_font,  # noqa: F821
            text_align=TextNode.ALeft,
            frameSize=(-0.02, 0.02, -2, 0.5),
            frameColor=(0, 0, 0, 0),
            pos=(-0.27, 0, 1.45),
        )
        self._pages = {"diary": [], "note": []}

        self._open_snd = loader.loadSfx("sounds/GUI/journal.ogg")  # noqa: F821
        self._page_snd = loader.loadSfx("sounds/GUI/journal_page.ogg")  # noqa: F821
        self._close_snd = loader.loadSfx("sounds/GUI/journal_close.ogg")  # noqa: F821

    def _open_page(self, type_, num):
        """Open the given page of the journal.

        Args:
            type_ (str): Page type: diary or note.
            num (int): Number of the page.
        """
        self._page_text["text"] = self._pages[type_][num]["page"]
        for page_type in ("diary", "note"):
            for page in self._pages[page_type]:
                page["but"]["text_fg"] = RUST_COL

        self._pages[type_][num]["but"]["text_fg"] = SILVER_COL
        self._page_snd.play()

    def add_page(self, num):
        """Add a page into the journal.

        Args:
            num (int): The page number.
        """
        type_, page_text = JOURNAL_PAGES[num]
        number = len(self._pages[type_]) + 1
        page_rec = {
            "page": page_text,
            "but": DirectButton(
                parent=self._main_fr,
                text="№" + str(number),
                text_font=base.main_font,  # noqa: F821
                text_fg=RUST_COL,
                text_shadow=(0, 0, 0, 1),
                frameColor=(0, 0, 0, 0),
                scale=(0.029, 0, 0.029),
                command=self._open_page,
                extraArgs=[type_, number - 1],
                pos=(-0.32 + number * 0.1, 0, 0.47 if type_ == "note" else 0.44,),
            ),
        }
        self._pages[type_].append(page_rec)

    def show(self):
        """Show/hide the journal GUI."""
        if self._is_shown:
            self._main_fr.hide()
            self._close_snd.play()
        else:
            self._main_fr.show()
            self._open_snd.play()

        self._is_shown = not self._is_shown
