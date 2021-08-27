"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The game text labels wirrten in Russian language.
"""

MAIN_MENU = (
    "Новая игра",
    "Загрузить",
    "Настройки",
    "Выход",
    (
        "Это альфа-сборка игры. Она не до конца сбалансирована, и"
        " некоторые её части ещё в разработке."
        "\nТаким образом, это концептуальный релиз для демонстрации основных "
        "идей. Приятной игры!"
    ),
    "Выберите команду",
    "Солдаты",
    "Рейдеры",
    "Анархисты",
    "Описание",
    "Начать",  # 10
    (
        "Солдаты - это люди крепкой дисциплины. Они отлично стреляют "
        "на средних\nдистанциях и хороши при атаке на укрепления. "
        "Их тактика строится на защите\nи развитии локомотива, "
        "вплоть до превращения его в передвижную крепость.\n\n"
        "Вы начнёте с 3 мужчинами. "
        "Лучший тип вылазок: Укрепление."
    ),
    (
        "Рейдеры привычны к трудностям и могут восстановиться после "
        "чего угодно. Они\nхороши в ближнем бою и умеют добывать "
        "ресурсы. Их тактика базируется на\nполучении и использовании "
        "расходуемых предметов и быстрой регенерации.\n\n"
        "Вы начнёте с 2 мужчинами и 1 женщиной. "
        "Лучший тип вылазок: Расхищение."
    ),
    (
        "Анархисты - это стихия самой природы! Они ценят тех, с кем их "
        "свела жизнь,\nи сплочаются намного быстрее других классов. "
        "Их тактика построена на\nнаборе людей, настройке "
        "их черт характера и командных навыках.\n\n"
        "Вы начнёте с 2 мужчинами и 1 женщиной. "
        "Лучший тип вылазок: Встреча."
    ),
    "Главное меню",
    "Сохранить игру",
    "(нельзя в бою)",
    "(нельзя у города)",
    "(нельзя у развилки)",
    "(нельзя при поражении)",
    "(нельзя в начале)",  # 20
    "Продолжить",
    "Разрешение:",
    "Обучение:",
    "Язык:",
    "Сохранить и перезагрузить",
    "Загрузка...",
    "Принять командование",
    (
        "Состояние Адъютанта критическое!\n"
        "Дальше он уже не поедет, а Смрад\n"
        "не заставит себя долго ждать.\n\n"
        "Всё кончено...",
    ),
)

KEYS_INFO = u"""
Управление:

Левая кнопка мыши - выбрать юнита/зону отдыха
Правая кнопка мыши - переместить юнита/указать цель
R - показать сплочение персонажа с другими

W - удерживать для ускорения
S - удерживать для замедления
F - включить прожекторы
M - показать схему дороги
J - открыть журнал

Камера:
\u2190\u2191\u2193\u2192 или толкнуть край экрана мышью - сдвинуть
Alt + \u2190\u2191\u2193\u2192 или удерживать колесо мыши - повернуть
"+", "-" или крутить колесо - приблизить/отдалить
C - центрировать камеру
"""

RESOURCES = (
    "Расходуемые предметы:",
    "Лекарство",
    "Лечит болезни и раны",
    "Фильтр дыма",
    "Снижает шанс стычки (5 мин.)",
    "Стимулятор",
    "Убирает плохие черты (5 мин.)",
    " км",
)

CHARACTERS = ("Имя:", "Класс:", "Здоровье", "Энергия", "Статус", "Черты")
CITY = (
    "Услуги",
    "Люди",
    "Поезд",
    "Покинуть",
    "Развернуться и покинуть",
    "Локомотив",
    "Ремонт",
    "Детали",
    "Поставить",
    "Экипаж",
    "Рекруты",  # 10
    "Предметы",
    "Исключить",
    "Нанять",
    "Продать",
    "Купить",
    """Правительство города выдаёт
Вам награду за помощь
в зачистке региона от
скинхедов.

Вы уничтожили:
""",
    "Награда всего:\n",
    """Жители города слышали о том,
как Ваш экипаж помог сиротам
построить лагерь. Они уважают
отзывчивых людей и поощряют
Вас - Адъютант получает 250
единиц Прочности бесплатно.""",
)

NOTES = (
    """Не забывайте сохраняться!""",
    """Выберите персонажа и нажмите
правую кнопку мыши на
другом, чтобы поменять
их местами""",
    """Персонаж может иметь до трёх
различных черт характера""",
    """Персонажи с высоким сплочением
могут случайным образом
перенимать черты друг
у друга""",
    """Скинхеды максимально
активны по вечерам""",
    """По утрам активность
скинхедов минимальна""",
    """Чем медленнее движется паровоз,
тем проще врагам попасть
в него метательным
оружием""",
    """Одни враги стреляют, другие
замедляют, третьи оглушают.
Изучайте их тактику!""",
    """Вражеская территория
не учитывается на схеме
Ж/Д путей""",
    """Правительства городов Сайлевера
поощрят Вас деньгами за
уничтожение скинхедов
поблизости""",
    # сплочение
    """Повышение общей сплочённости
открывает навыки экипажа. Это
сильные временные эффекты,
которые помогут Вам выжить.""",
    """Солдаты и рейдеры не любят друг
друга. Построить сплочение
между ними будет сложно.""",
    """Чтобы увеличить сплочение
между конкретными персонажами,
держите их ближе друг
к другу""",
    # вылазки
    """Хороший способ увеличить
сплочение между конкретными
персонажами - это послать
их вместе на вылазку""",
    """Даже слабый результат на
вылазке может быть
полезным - персонажи
сплочатся""",
    """Разные типы вылазок дают
разные виды трофеев""",
    """Вылазка может стать очень
опасной. Лучше отправлять
на неё людей, хорошо
знакомых друг с другом.""",
    """Вы не можете командовать своими
людьми, пока они на вылазке.
Вы можете только отправить
подходящих людей.""",
    """Вылазка может как обернуться
опасностью, так и оказаться
плёвым делом. Рискуйте!""",
    """Рекруты, найденные на вылазках
типа Встреча, запрашивают
меньшее вознаграждение,
чем в городах""",
    """Нажмите M, чтобы посмотреть
на схему Ж/Д путей и
спланировать маршрут""",
    """Ж/Д ветки всегда соединяются
обратно в главную
магистраль""",
    """Вы можете развернуться в городе.
Учитывайте это во время
планирования маршрута.""",
    """Останавливаться на вражеской
территории безрассудно""",
    """Включение освещения поможет Вам
сохранить энергию персонажей и
повысить точность их стрельбы,
но так же привлечёт внимание""",
    """Изношенные ржавые рельсы
могут сильно повредить колёса
локомотива. Сбросьте скорость,
если слышите скрип металла.""",
    """Активные орудия локомотива
можно использовать только
на вражеской территории""",
    """Женщины милы и социальны. Они
снижают стресс в любом
коллективе.""",
    """У женщин меньше здоровья, но
они куда энергичнее""",
    """Люди устают быстрее в темноте
и во время боя""",
    # raiders
    """Жизнь рейдеров полна грабежа.
Они умеют находить полезные
ресурсы и предметы.""",
    """Рейдеры - хорошие стрелки на
короткой дистанции""",
    """Рейдеры растрачивают энергию
быстро, но они так же
быстро отдыхают""",
    # soldiers
    """Солдаты - хорошие стрелки на
средней дистанции""",
    """Если Вы хотите ударить по
вражеским укрепления,
солдаты - это Ваш выбор""",
    # anarchists
    """Анархисты демократичны. Они
выстраивают сплочение
быстрее других""",
    """Анархисты получают множитель
урона x2 от сплочения""",
    """Анархисты - это люди толпы.
Они ценят тех, с кем их
свела жизнь.""",
    # accuracy
    """Точность стрельбы зависит от
освещения, дистанции,
класса персонажа и
его энергии""",
    """Отправьте персонажа в Зону
Отдыха локомотива. Отдых
восстанавливает здоровье
и энергию.""",
    # diseases
    """Болезни снижают максимум
энергии персонажа до 80 и
отключают все его
положительные черты""",
    """Ограничьте контакты больного
персонажа с другими, чтобы
остановить распространение
инфекции""",
    """Раненные и уставшие персонажи
более уязвимы для болезней""",
    # the Stench
    """Оранжевые облака Смрада
очень ядовиты. Пересекайте
их как можно быстрее!""",
    # resources
    """Стимулятор временно отключает
негативные черты юнита.
Так же он даёт иммунитет
к оглушению.""",
)

DEFAULT_NOTE = "Нажмите F1, чтобы открыть\nсправку по управлению"

TIPS = ("Отдыхают:", "Зона отдыха", "Приближаемся к городу")

COHESION = (
    "Навыки экипажа",
    "Вспомним былое",
    "Каждый юнит получает +10 энергии. Зарядка: 4 мин.",
    "Прикрывающий огонь",
    "Каждый юнит получает +20% точности. Зарядка: 5 мин.",
    "Своих не бросаем",
    "Юниты со здоровьем < 30 получают +25 здоровья. Зарядка: 10 мин.",
    "Общая ярость",
    "Каждый юнит получает +30% к урону. Зарядка: 10 мин.",
    "Держимся, вместе",
    "Ни один юнит не погибнет в следующие 1.5 мин. Зарядка: 15 мин.",
)

DISTINGUISHED = (
    "Лист отличившихся",
    (
        "Здесь Вы можете хвалить и отчитывать своих людей, "
        "чтобы изменить их черты.\nУказание на личность часто "
        "вредит атмосфере в коллективе, поэтому\nкаждое действие "
        "будет немного сокращать общую сплочённость команды.\n\n"
        "Выберите одну из черт текущего персонажа (положительную "
        "или отрицательную)\nи отчитайте юнита, чтобы убрать её. "
        "Это будет стоить 4 очка сплочения.\n\n"
        "Если у юнита менее трёх черт, Вы можете похвалить его, "
        "чтобы\nсгенерировать 3 новые черты и добавить одну из них "
        "текущему юниту.\nЭто будет стоить Вам 4 очка сплочения."
    ),
    "Очков сплочения:",
    "Новые черты:",
    "Похвалить",
    "Отчитать",
    "Готово",
    "Текущие черты",
)

SPLASHES = (
    "Напутствие от автора",
    """Forward Only не наказывает сразу, но каждая ошибка
затягивает петлю сильнее. Планируйте наперёд!""",
)

MECHANIC_DESC = {
    "локомотив": {
        "descs": (
            (
                "Это Адъютант - Ваш локомотив, он едет достаточно\n"
                "быстро, чтобы обогнать смерть. Берегите его -\n"
                "приди он в негодность, и Ваши часы сочтены! Его\n"
                "Прочность указана в правом нижнем углу экрана.\n"
                "Ржавые рельсы могут повредить Вам колёса -\n"
                "замедлитесь, если слышите металлический скрип."
            ),
            (
                "Адъютант состоит из трёх частей и Зоны Отдыха,\n"
                "по которым Вы можете расставлять своих людей.\n"
                "Мудрая ротация юнитов - залог Вашего успеха.\n\n"
                "Скорость указана в правом нижнем углу экрана.\n"
                "Удерживайте W и S для ускорения и замедления."
            ),
        ),
        "previews": ("locomotive1", "locomotive2"),
    },
    "персонажи": {
        "descs": (
            (
                "В Вашем экипаже нескольких бойцов. У каждого\n"
                "юнита есть энергия, поддерживайте её на высоком\n"
                "уровне, т.к. она влияет на точность стрельбы и\n"
                "результат на вылазках. Лучший способ восполнить\n"
                "энергию и здоровье юнита - это дать ему отдохнуть."
            ),
            (
                "Кликните ЛКМ на юните, чтобы выбрать его, затем\n"
                "ПКМ на одной из стрелок, чтобы переместить\n"
                "юнита в соответствующую часть локомотива; или\n"
                "кликните ПКМ на Зоне Отдыха, чтобы он отдохнул.\n"
                "Кол-во мест в каждой части локомотива ограничено."
            ),
        ),
        "previews": ("characters1", "characters2",),
    },
    "Смрад": {
        "descs": (
            (
                "Смрад - это главная проблема. Его ядовитые облака\n"
                "расползаются быстро, хаотично, и, вероятно,\n"
                "он покроет весь Сайлевер за пару недель.\n"
                "Если Вы попали в облако, ускорьтесь, чтобы\n"
                "поскорее пересечь его. Так же не стоит долго\n"
                "стоять на одном месте или ездить кругами."
            ),
            (
                "Ищите способ пережить Смрад! В Сайлевере есть\n"
                "несколько мест интереса - посетите как можно\n"
                "больше из них, чтобы получить полезные данные.\n"
                "Используйте карту (клавиша M), чтобы построить\n"
                "оптимальный маршрут. На карте Вы так же можете\n"
                "увидеть вылазки и покрытие Сайлевера Смрадом."
            ),
        ),
        "previews": ("the_stench1", "map"),
    },
    "сплочение": {
        "descs": (
            (
                "Ваши юниты со временем вырабатывают сплочение.\n"
                "Общая сплочённость экипажа показана в правом\n"
                "верхнем углу экрана. Наращивание сплочения\n"
                "открывает навыки экипажа - сильные временные\n"
                "эффекты, оказывающие влияние на каждого юнита.\n"
            ),
            (
                "Стоит держать юнитов с высоким сплочением на\n"
                "одной части локомотива, тогда они получат бонус\n"
                "к силе. Сплочение растёт быстрее между юнитами\n"
                "на одной части локомотива. Увидеть сплочение\n"
                "юнита с другими можно, выбрав его и нажав R."
            ),
        ),
        "previews": ("cohesion1", "cohesion2"),
    },
    "вылазки": {
        "descs": (
            (
                "Вылазки - основной источник денег и других\n"
                "ресурсов. Это событие, которое требует остановки\n"
                "и отправки нескольких юнитов. Существует 3 типа\n"
                "вылазок: Встреча, Расхищение и Укрепление, каждая\n"
                "с определённым типом трофеев и требованием\n"
                "определённого класса юнитов."
            ),
            (
                "У каждой вылазки 5 исходов; чем больше очков\n"
                "набрано, тем лучше исход. Очки начисляются за:\n"
                "классы отправленных юнитов, их состояние -\n"
                "здоровье и энергия, за сплочение между ними\n"
                "и 0-10 случайно набираемых очков."
            ),
        ),
        "previews": ("outings1", "outings2"),
    },
    "предметы": {
        "descs": (
            (
                "Вы можете найти предметы на вылазках или на\n"
                "рынках городов. Выберите юнита и кликните на\n"
                "кнопку предмета, чтобы использовать его. Деньги\n"
                "- это основной ресурс, Вы можете тратить их в\n"
                "городах на починку и апгрейд локомотива,\n"
                "лечение и отдых, наём новых людей."
            ),
        ),
        "previews": ("resources1",),
    },
    "состояние юнита": {
        "descs": (
            (
                "У каждого юнита может быть до трёх черт\n"
                "(хороших или плохих). Черты дают преимущества\n"
                "или слабости в разных ситуациях. Вы можете\n"
                "изменить черты юнита в Листе Отличившихся, но\n"
                "это понизит сплочённость команды на время."
            ),
            (
                "Текущие эффекты, влияющие на юнита, отражены\n"
                "в его Статусе. Так же следите за иконкой\n"
                "болезни - больной юнит может принести много\n"
                "проблем экипажу. Постарайтесь изолировать\n"
                "заражённого и вылечить его как можно скорее."
            ),
        ),
        "previews": ("character_status1", "character_status2"),
    },
}

MECHANIC_NAMES = (
    "локомотив",
    "персонажи",
    "Смрад",
    "сплочение",
    "вылазки",
    "предметы",
    "состояние юнита",
)

MECHANIC_BUTS = ("Далее", "Принято!")

CLASS_DESCS = {
    "MotoShooter": {
        "desc": (
            "Мотострелок постарается выпустить в Вас\n"
            "и локомотив столько пуль, сколько сможет.\n"
            "Большинство скинхедов предпочитают такой\n"
            "способ общения с иностранцами, так что\n"
            "сохраняйте бдительность - их будет много.\n"
        ),
        "preview": "shooter",
        "but_text": "Принято!",
        "title": "Скинхеды ищут Вас!",
    },
    "BrakeThrower": {
        "desc": (
            "Башмачник постарается обогнать Вас и бросить\n"
            "тормозной башмак Вам под колёса, чтоб замедлить.\n"
            "Эти парни не особо сильны сами по себе, но\n"
            "они могут сделать атаки других скинхедов\n"
            "успешнее. Старайтесь убивать их первыми!"
        ),
        "preview": "brake_thrower",
        "but_text": "Понятно!",
        "title": "Скинхеды обсуждают дерзких новичков!",
    },
    "Barrier": {
        "desc": (
            "Скинхеды стали использовать барьеры против\n"
            "Вас. Барьер может нанести много урона локомотиву\n"
            "при столкновении. Рекомендуется установить\n"
            "Таран в ближайшем городе, чтобы обеспечить\n"
            "себя хорошей защитой от них."
        ),
        "preview": "barrier",
        "but_text": "Мы справимся!",
        "title": "Скинхеды начали расставлять барьеры!",
    },
    "StunBombThrower": {
        "desc": (
            "Такой боец будет бросать оглушающие шашки,\n"
            "чтобы обездвижить Ваших людей на несколько\n"
            "секунд. Ему будет сложно попасть по быстро\n"
            "движущемуся локомотиву, но если Вы потеряете\n"
            "часть скорости, точность его бросков повысится."
        ),
        "preview": "bomb_thrower",
        "but_text": "Мы готовы!",
        "title": "Скинхеды начали воспринимать Вас всерьёз!",
    },
    "DodgeShooter": {
        "desc": (
            "Dodge с пулемётом - это сильный враг. Он может\n"
            "нанести много урона локомотиву, но его орудие\n"
            "быстро перегревается и требует паузы на\n"
            "охлаждение. Рекомендуется установить Пластину\n"
            "Брони, чтобы защититься от этого типа врага."
        ),
        "preview": "dodge",
        "but_text": "Ясно!",
        "title": "Скинхеды собирают технику, чтобы достать Вас!",
    },
    "Rocket": {
        "desc": (
            "Ваш прогресс приводит скинхедов в бешенство!\n"
            "Они бросают всё больше сил на Вас. Их последняя\n"
            "идея - телеуправляемые ракеты, могут серьёзно\n"
            "навредить локомотиву. Используйте Пластину\n"
            "Брони, чтобы защитить целевую сторону поезда."
        ),
        "preview": "rocket",
        "but_text": "Нас не остановить!",
        "title": "Скинхеды начали использовать ракеты!",
    },
    "Kamikaze": {
        "desc": (
            "На Вас идут камикадзе! Они могут нанести большой\n"
            "урон Адъютанту, но только один раз. Рекомендуется\n"
            "установка Пластины Брони. Так же можно уничтожать\n"
            "камикадзе до того, как они зажигают фитиль. Если\n"
            "улучить момент, взрыв камикадзе нанесёт урон\n"
            "другим врагам поблизости!"
        ),
        "preview": "kamikaze",
        "but_text": "Переживём!",
        "title": "Все силы скинхедов направлены на Вас!",
    },
}

SCHEME = (
    "Ж/Д схема Сайлевера",
    "Обозначения:\nm - Встреча\nl - Расхищение\ne - Укрепление\ni - Место интереса",
    "   - город",
    "- Ж/Д ветка",
    "- Смрад",
)

TRAITS = [
    ("Шустрость", "Улитка"),
    ("Сова", "Страх темноты"),
    ("Мазохизм", "Гемофобия"),
    ("Иммунитет", "Тепличность"),
    ("Либерализм", "Одиночка"),
    ("Жестокость", "Нервозность"),
    ("Ныряльщик", "Морская болезнь"),
    ("Механик", "Фармакофобия"),
]

TRAIT_DESC = {
    "Шустрость": "+30% скорость стрельбы",
    "Улитка": "-20% скорость стрельбы",
    "Сова": "+25% точность в темноте",
    "Страх темноты": "+50% затрат энергии в темноте",
    "Мазохизм": "С уроном восполняет энергию",
    "Гемофобия": "+25% затрат энергии, если здоровье < 50%",
    "Иммунитет": "-40% шанс заболеть",
    "Тепличность": "+20% шанс заболеть",
    "Либерализм": "+30% рост сплочения с другими классами",
    "Одиночка": "x1.3 урона, если один на части поезда",
    "Жестокость": "+7 здоровья за уничтожение врага",
    "Нервозность": "+25% затрат энергии в бою",
    "Ныряльщик": "Не вдыхает Смрад в течении 1 мин.",
    "Морская болезнь": "Не отдыхает на высокой скорости",
    "Механик": "Чинит локомотив, если не отдыхает",
    "Фармакофобия": "Лечится на 40% медленнее",
}

UPGRADES_DESC = {
    "Таран": {
        "name": "Таран",
        "desc": """С тараном Ваш локомотив
будет сбивать барьеры,
не получая никакого урона""",
        "cost": "120$",
        "model": "ram1",
        "threshold": 1,
    },
    "Прожекторы": {
        "name": "Прожекторы",
        "desc": """Все негативные факторы
темноты станут неактуальны
с этими прожекторами""",
        "cost": "190$",
        "model": "floodlights1",
        "threshold": 2,
    },
    "Пластина Брони": {
        "name": "Пластина Брони",
        "desc": """Активный щит, закрывает
одну сторону локомотива.
Нажмите 4, 5, 6, чтобы двигать.""",
        "cost": "70$",
        "model": "armor_plate",
        "threshold": 1,
    },
    "Огнетушители": {
        "name": "Огнетушители",
        "desc": """Постепенно повышает
Прочность поезда до 400 ед.
в случае большого урона""",
        "cost": "190$",
        "model": "fire_extinguishers",
        "threshold": 2,
    },
    "Гранатомёт": {
        "name": "Гранатомёт",
        "desc": """Активное орудие, наносит
урон по области. Нажмите
1, чтобы активировать.""",
        "cost": "180$",
        "model": "grenade_launcher",
        "threshold": 1,
    },
    "Место": {
        "name": "Место",
        "desc": """Добавляет одну ячейку
юнита в зону отдыха
локомотива""",
        "cost": "140$",
        "model": "sleeper1",
        "threshold": 1,
    },
    "Оконные Рамы": {
        "name": "Оконные Рамы",
        "desc": """С этим оконными рамами
юниты в зоне отдыха будут
защищены от Смрада""",
        "cost": "150$",
        "model": "isolation",
        "threshold": 2,
    },
    "Ракетомёт": {
        "name": "Ракетомёт",
        "desc": """Пускает ракеты, которые
разделяются на 4 гранаты
и наносят урон в 4-х местах.
Нажмите 3, чтобы стрелять.""",
        "cost": "200$",
        "model": "cluster_bomb_launcher",
        "threshold": 2,
    },
    "Пулемёт": {
        "name": "Пулемёт",
        "desc": """Даёт прицельный залп.
Лучше стрелять по одной цели.
Нажмите 2, чтобы стрелять.""",
        "cost": "160$",
        "model": "machine_gun",
        "threshold": 2,
    },
    "Протекторы": {
        "name": "Протекторы",
        "desc": """Броня для колёс и толкающего
механизма. Повышает макс.
Прочность до 150%.""",
        "cost": "160$",
        "model": "armor",
        "threshold": 1,
    },
}

FORKS = (
    "Подъезжаем к стрелке:\nповерните вправо - T,\nили игнорируйте",
    "Подъезжаем к стрелке:\nповерните влево - T,\nили игнорируйте",
)

JOURNAL = ("Журнал", "Листы", "Очерк")
