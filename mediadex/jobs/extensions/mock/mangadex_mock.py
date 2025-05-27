from ..interfaces.manga_source import MangaSource


class MangaDexSourceMock(MangaSource):
    def get_popular_manga(self, page: int = 1):
        return mock_get_popular_manga

    def search(self, query: str):
        """Search for manga, returns list of dict {title, url}"""
        pass

    def get_chapters(self, manga_url: str):
        """Returns the list of chapters for a given manga"""
        pass

    def get_pages(self, chapter_url: str):
        """Returns the list of page URLs for a chapter"""
        pass

mock_get_popular_manga = [
    {
        "title": "My Dress-Up Darling",
        "url": "/manga/aa6c76f7-5f5f-46b6-a800-911145f81b9b",
        "description": "Wakana Gojou is a fifteen year old high-school boy who was socially traumatized in the past due to his passions. That incident left a mark on him that made him into a social recluse. Until one day he had an encounter with Kitagawa who is a sociable gyaru, who is the complete opposite of him. They soon share their passions with one another which leads to their odd relationship.",
        "cover_url": "https://uploads.mangadex.org/covers/aa6c76f7-5f5f-46b6-a800-911145f81b9b/2fffbe0f-a5c5-4365-a0ba-98e8431c71de.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "completed",
        "tags": [
            "Romance",
            "Comedy",
            "Drama",
            "School Life",
            "Slice of Life",
            "Gyaru"
        ],
        "year": 2018,
        "original_language": "ja",
        "manga_id": "aa6c76f7-5f5f-46b6-a800-911145f81b9b"
    },
    {
        "title": "Kage no Jitsuryokusha ni Naritakute!",
        "url": "/manga/77bee52c-d2d6-44ad-a33a-1734c1fe696a",
        "description": "Just like how everyone adored heroes in their childhood, a certain young man adored those powers hidden in shadows. Ninjas, rogues, shadowy mentor types, that sort of deal.  \r\nAfter hiding his strength and living the mediocre life of a NPC by day while undergoing frenzied training by night, he finally reincarnates into a different world and gains ultimate power.  \r\nThe young man who is only pretending to be a power in the shadows\u2026 his subordinates who took him more seriously than he expected\u2026 and a giant organization in the shadows that gets accidentally trampled\u2026  \r\nThis is the story of a young boy who had adored powers in shadows possibly eventually reigning over the world of shadows in another world.",
        "cover_url": "https://uploads.mangadex.org/covers/77bee52c-d2d6-44ad-a33a-1734c1fe696a/3e07507b-3425-48ee-baf0-83603a098487.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Reincarnation",
            "Action",
            "Demons",
            "Comedy",
            "Martial Arts",
            "Magic",
            "Harem",
            "Isekai",
            "Drama",
            "School Life",
            "Fantasy",
            "Adaptation"
        ],
        "year": 2018,
        "original_language": "ja",
        "manga_id": "77bee52c-d2d6-44ad-a33a-1734c1fe696a"
    },
    {
        "title": "Tensei Shitara Slime Datta Ken",
        "url": "/manga/e78a489b-6632-4d61-b00b-5206f5b8b22b",
        "description": "The ordinary Mikami Satoru found himself dying after being stabbed by a slasher. It should have been the end of his meager 37 years, but he found himself deaf and blind after hearing a mysterious voice.  \nHe had been reincarnated into a slime!  \n  \nWhile complaining about becoming the weak but famous slime and enjoying the life of a slime at the same time, Mikami Satoru met with the Catastrophe-level monster \u201cStorm Dragon Veldora\u201d, and his fate began to move.\n\n---\n**Links:**\n- Alternative Official English - [K MANGA](https://kmanga.kodansha.com/title/10044/episode/317350) (U.S. Only), [INKR](https://comics.inkr.com/title/233-that-time-i-got-reincarnated-as-a-slime), [Azuki](https://www.azuki.co/series/that-time-i-got-reincarnated-as-a-slime), [Coolmic](https://coolmic.me/titles/587), [Manga Planet](https://mangaplanet.com/comic/618e32db10673)",
        "cover_url": "https://uploads.mangadex.org/covers/e78a489b-6632-4d61-b00b-5206f5b8b22b/67de8b2f-c080-4006-91dd-a3b87abdb7fd.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Reincarnation",
            "Monsters",
            "Action",
            "Demons",
            "Comedy",
            "Samurai",
            "Isekai",
            "Fantasy",
            "Adaptation"
        ],
        "year": 2015,
        "original_language": "ja",
        "manga_id": "e78a489b-6632-4d61-b00b-5206f5b8b22b"
    },
    {
        "title": "Chainsaw Man",
        "url": "/manga/a77742b1-befd-49a4-bff5-1ad4e6b0ef7b",
        "description": "Broke young man + chainsaw dog demon = Chainsaw Man!  \n  \nThe name says it all! Denji's life of poverty is changed forever when he merges with his pet chainsaw dog, Pochita! Now he's living in the big city and an official Devil Hunter. But he's got a lot to learn about his new job and chainsaw powers!",
        "cover_url": "https://uploads.mangadex.org/covers/a77742b1-befd-49a4-bff5-1ad4e6b0ef7b/bf31b6c3-9075-4c1e-95be-b6a38ffed10f.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Award Winning",
            "Monsters",
            "Action",
            "Demons",
            "Comedy",
            "Gore",
            "Horror",
            "Supernatural"
        ],
        "year": 2018,
        "original_language": "ja",
        "manga_id": "a77742b1-befd-49a4-bff5-1ad4e6b0ef7b"
    },
    {
        "title": "Komi-san wa Komyushou Desu.",
        "url": "/manga/a96676e5-8ae2-425e-b549-7f15dd34a6d8",
        "description": "Komi-san is a beautiful and admirable girl that no one can take their eyes off of. Almost the whole school sees her as the cold beauty that's out of their league, but Tadano Hitohito knows the truth: she's just really bad at communicating with others.\n\nKomi-san, who wishes to fix this bad habit of hers, tries to improve it with the help of Tadano-kun by achieving her goal of having 100 friends.\n\n---\n**Links:**\n- Alternative Official English - [VIZ Manga Chapters](https://www.viz.com/vizmanga/chapters/komi-cant-communicate)",
        "cover_url": "https://uploads.mangadex.org/covers/a96676e5-8ae2-425e-b549-7f15dd34a6d8/f8f44329-1dd7-4301-9ec7-a4a76182e8eb.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "completed",
        "tags": [
            "Award Winning",
            "Romance",
            "Comedy",
            "School Life",
            "Slice of Life"
        ],
        "year": 2016,
        "original_language": "ja",
        "manga_id": "a96676e5-8ae2-425e-b549-7f15dd34a6d8"
    },
    {
        "title": "Mushoku Tensei ~Isekai Ittara Honki Dasu~",
        "url": "/manga/bd6d0982-0091-4945-ad70-c028ed3c0917",
        "description": "A 34-year-old NEET gets killed in a traffic accident and finds himself in a world of magic. Rather than waking up as a full-grown mage, he gets reincarnated as a newborn baby, retaining the memories of his past life. Before he can even properly move his body, he resolves to never make the same mistakes he made in his first life ever again and instead live a life with no regrets with the new one that was given to him. Because he has the knowledge of a middle-aged man, by the age of two, he has already become a prodigy and possesses power unthinkable for anyone his age and even older. Thus begins the chronicles of Rudeus Greyrat, son of swordsman Paul and healer Zenith, as he enters a new world to become the strongest mage known to man, with powers rivaling even the gods themselves.",
        "cover_url": "https://uploads.mangadex.org/covers/bd6d0982-0091-4945-ad70-c028ed3c0917/0194b8a6-727d-45b9-ba3c-94c08921405d.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Reincarnation",
            "Action",
            "Romance",
            "Comedy",
            "Adventure",
            "Magic",
            "Harem",
            "Isekai",
            "Drama",
            "Fantasy",
            "Adaptation"
        ],
        "year": 2014,
        "original_language": "ja",
        "manga_id": "bd6d0982-0091-4945-ad70-c028ed3c0917"
    },
    {
        "title": "One-Punch Man",
        "url": "/manga/d8a959f7-648e-4c8d-8f23-f1f3f8e129f3",
        "description": "After rigorously training for three years, the ordinary Saitama has gained immense strength which allows him to take out anyone and anything with just one punch. He decides to put his new skill to good use by becoming a hero. However, he quickly becomes bored with easily defeating monsters, and wants someone to give him a challenge to bring back the spark of being a hero.  \n  \nUpon bearing witness to Saitama's amazing power, Genos, a cyborg, is determined to become Saitama's apprentice. During this time, Saitama realizes he is neither getting the recognition that he deserves nor known by the people due to him not being a part of the Hero Association. Wanting to boost his reputation, Saitama decides to have Genos register with him, in exchange for taking him in as a pupil. Together, the two begin working their way up toward becoming true heroes, hoping to find strong enemies and earn respect in the process.  \n  \n\n\n\n---\n\n**Notes:**  \n- Because some groups use the web version of the manga while others use the magazine version, the numbering won't match between different languages.  \n- **Because a takedown notice was sent to MangaDex from the owners of this series, fan translations of One Punch Man are currently unavailable to be uploaded. The series can be read in its entirety at [the official Shonen Jump website,](https://www.viz.com/shonenjump/chapters/one-punch-man) with the first and latest three chapters available at any time and the rest accessible with a Shonen Jump membership (which costs about $2 a month and can be accessed via a VPN if you are outside the US).**",
        "cover_url": "https://uploads.mangadex.org/covers/d8a959f7-648e-4c8d-8f23-f1f3f8e129f3/361c2d3a-9c43-4cf7-824e-62eddb9f56a0.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Award Winning",
            "Sci-Fi",
            "Monsters",
            "Action",
            "Comedy",
            "Superhero",
            "Martial Arts",
            "Gore",
            "Drama",
            "Supernatural",
            "Mystery"
        ],
        "year": 2012,
        "original_language": "ja",
        "manga_id": "d8a959f7-648e-4c8d-8f23-f1f3f8e129f3"
    },
    {
        "title": "Ijiranaide, Nagatoro-san",
        "url": "/manga/d86cf65b-5f6c-437d-a0af-19a31f94ec55",
        "description": "Naoto Hachiouji \u2014our spineless\u2014 MC (Known also as \"Senpai\") is a second-year high school student and a loner who spends his afternoons at the Arts Club room. He attracts the attention of one of his schoolmates, a sadistic freshman girl named Nagatoro. However, in between the bullying and teasing, something else begins to blossom.\n\nA lovey-dovey(\u2026?) story between a shy nerd and an S-Dere (Sadistic Tsundere) begins.\n\n---\n\n**Links:**\n\n- Alternative Official English - [K Manga](https://kmanga.kodansha.com/title/10042/episode/313808) (U.S. Only), [Kodansha](https://kodansha.us/series/dont-toy-with-me-miss-nagatoro/)",
        "cover_url": "https://uploads.mangadex.org/covers/d86cf65b-5f6c-437d-a0af-19a31f94ec55/5e4a4e0e-b2a6-4e7e-8e6e-169a8d26c7a8.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "completed",
        "tags": [
            "Romance",
            "Comedy",
            "School Life",
            "Slice of Life",
            "Gyaru"
        ],
        "year": 2017,
        "original_language": "ja",
        "manga_id": "d86cf65b-5f6c-437d-a0af-19a31f94ec55"
    },
    {
        "title": "Otome Game Sekai wa Mob ni Kibishii Sekai desu",
        "url": "/manga/28c77530-dfa1-4b05-8ec3-998960ba24d4",
        "description": "Leon, a former Japanese worker, was reincarnated into an \u201cotome game\u201d world, and despaired at how it was a world where females hold dominance over males. It was as if men were just livestock that served as stepping stones for females in this world. The only exceptions were the game\u2019s romantic targets, a group of handsome men led by the crown prince. In these bizarre circumstances, Leon held one weapon: his knowledge from his previous world, where his brazen sister had forced him to complete this game. This is a story about his adventure to survive and thrive in this world.",
        "cover_url": "https://uploads.mangadex.org/covers/28c77530-dfa1-4b05-8ec3-998960ba24d4/2a87c2b5-83ab-4cfa-96fd-da840f6f0e6f.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "hiatus",
        "tags": [
            "Reincarnation",
            "Sci-Fi",
            "Action",
            "Romance",
            "Comedy",
            "Mecha",
            "Adventure",
            "Video Games",
            "Magic",
            "Harem",
            "Isekai",
            "Drama",
            "School Life",
            "Fantasy",
            "Villainess",
            "Delinquents",
            "Slice of Life",
            "Supernatural",
            "Adaptation"
        ],
        "year": 2018,
        "original_language": "ja",
        "manga_id": "28c77530-dfa1-4b05-8ec3-998960ba24d4"
    },
    {
        "title": "Lv2 kara Cheat datta Moto Yuusha Kouho no Mattari Isekai Life",
        "url": "/manga/58bc83a0-1808-484e-88b9-17e167469e23",
        "description": "Banaza, who was summoned to the magic kingdom of Cryroad as a Hero candidate, was disqualified as a Hero because of his ordinary abilities. He was supposed to be returned to his original world, but due to the magical kingdom's mistake, he became unable to return to his original world. However, the moment he reached Level 2, he acquired every single possible skill and kind of magic, turning him into a super cheat with infinite skills! Despite this, he takes Fenris of the demons as his wife, and fully enjoys his newly-married life with an easygoing smile. He changes his name to Fulio and tries to lead his life quietly, but things are a bit chaotic with the likes of a pet saber, four freeloading female knights, a Majin, and even an ex-Demon Lord. However, even with all of this chaos, he still manages to enjoy his life peacefully.",
        "cover_url": "https://uploads.mangadex.org/covers/58bc83a0-1808-484e-88b9-17e167469e23/8ed55e27-f160-41c5-9cab-8f4551b1dfa1.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Monsters",
            "Action",
            "Demons",
            "Romance",
            "Comedy",
            "Adventure",
            "Magic",
            "Isekai",
            "Drama",
            "Fantasy",
            "Monster Girls",
            "Slice of Life",
            "Adaptation"
        ],
        "year": 2019,
        "original_language": "ja",
        "manga_id": "58bc83a0-1808-484e-88b9-17e167469e23"
    },
    {
        "title": "Kumo Desu ga, Nani ka?",
        "url": "/manga/eb2d1a45-d4e7-4e32-a171-b5b029c5b0cb",
        "description": "When a mysterious explosion killed an entire class full of high school students, the souls of everyone in class were transported into a fantasy world and reincarnated. While some students were reincarnated as princes or prodigies, others were not as blessed.  \nOur heroine, who was the lowest in the class, discovered that she was reincarnated as a spider! Now at the bottom of the food chain, she needs to adapt to the current situation with willpower in order to live. Stuck in a dangerous labyrinth filled with monsters, it's eat or be eaten!  \nThis is the story of a spider doing whatever she can in order to survive!",
        "cover_url": "https://uploads.mangadex.org/covers/eb2d1a45-d4e7-4e32-a171-b5b029c5b0cb/1c3917ec-7cb3-4786-bcf2-d259c89562d7.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Reincarnation",
            "Monsters",
            "Action",
            "Demons",
            "Comedy",
            "Survival",
            "Adventure",
            "Magic",
            "Isekai",
            "Drama",
            "Fantasy",
            "Monster Girls",
            "Adaptation"
        ],
        "year": 2015,
        "original_language": "ja",
        "manga_id": "eb2d1a45-d4e7-4e32-a171-b5b029c5b0cb"
    },
    {
        "title": "Tsuki ga Michibiku Isekai Douchuu",
        "url": "/manga/7643e9f6-8455-4a58-b7e8-bf6cd00f5251",
        "description": "High school student Misumi Makoto is called into a fantasy world by the god Tsukuyomi, in order to be a hero. However, powerful others in this world aren't as thrilled to have him there, and they kick him to the edge of the world just as Tsukuyomi declares that he must leave Makoto to find his own way. Now it's up to Makoto to find his own way!\n___\n[Official English Light Novel](https://hanashi.media/tsukimichi-moonlit-fantasy/)",
        "cover_url": "https://uploads.mangadex.org/covers/7643e9f6-8455-4a58-b7e8-bf6cd00f5251/51db61cc-d21a-47da-b6d4-6a0ae6637c9b.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Monsters",
            "Action",
            "Demons",
            "Comedy",
            "Adventure",
            "Magic",
            "Harem",
            "Isekai",
            "Gore",
            "Drama",
            "Fantasy",
            "Monster Girls",
            "Adaptation"
        ],
        "year": 2015,
        "original_language": "ja",
        "manga_id": "7643e9f6-8455-4a58-b7e8-bf6cd00f5251"
    },
    {
        "title": "Akuyaku Reijou Level 99: Watashi wa UraBoss desu ga Maou de wa Arimasen",
        "url": "/manga/878634d2-ea39-4001-a4bf-31458020d16a",
        "description": "I reincarnated as the \"Villainess Eumiella\" from an RPG Otome game. In the main story, Eumiella is merely a side character, but after the ending, she re-enters the story as the Hidden Boss, a character boasting high stats on par with the heroes! \n\nLighting a fire in my gamer's soul, and taking advantage of being left on my own in my parent's territory, I trained, trained, and trained! As a result of my training\u2026 by the time I enrolled in the academy, I managed to reach level 99. \n\nThough I had planned to live out my days as inconspicuously and peacefully as possible, soon after entering the school, I'm suspected by the Heroine and Love Interests of being the \"Demon Lord\"\u2026?  \n  \nBased on a popular web novel of seeking a peaceful life, a fantasy story of the strongest villainess!\n\n---\n**Links:**\n- Alternative Official Raw - [Niconico](https://manga.nicovideo.jp/comic/46067)",
        "cover_url": "https://uploads.mangadex.org/covers/878634d2-ea39-4001-a4bf-31458020d16a/ab903f92-b3d9-4ce3-9332-d5cffa35cf67.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Reincarnation",
            "Monsters",
            "Action",
            "Demons",
            "Romance",
            "Comedy",
            "Video Games",
            "Magic",
            "Isekai",
            "School Life",
            "Fantasy",
            "Villainess",
            "Adaptation"
        ],
        "year": 2020,
        "original_language": "ja",
        "manga_id": "878634d2-ea39-4001-a4bf-31458020d16a"
    },
    {
        "title": "Mieruko-chan",
        "url": "/manga/6670ee28-f26d-4b61-b49c-d71149cd5a6e",
        "description": "All of a sudden, Miko is able to see grotesque monsters all around her; but no one else can. Rather than trying to run away or face them, she instead musters all of her courage and... ignores them. Join in on her day-to-day life as she keeps up her best poker face despite the supernatural goings-on.\n___\n**Alt Official Raw:** [niconico Manga](http://manga.nicovideo.jp/comic/37662)",
        "cover_url": "https://uploads.mangadex.org/covers/6670ee28-f26d-4b61-b49c-d71149cd5a6e/bd7e79a1-5a29-46e8-b402-765e7f01ff9b.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Award Winning",
            "Monsters",
            "Psychological",
            "Ghosts",
            "Comedy",
            "Magic",
            "Gore",
            "Drama",
            "School Life",
            "Horror",
            "Slice of Life",
            "Supernatural",
            "Mystery",
            "Tragedy"
        ],
        "year": 2018,
        "original_language": "ja",
        "manga_id": "6670ee28-f26d-4b61-b49c-d71149cd5a6e"
    },
    {
        "title": "Kaette Kudasai! Akutsu-san",
        "url": "/manga/737a846b-2e67-4d63-9f7e-f54b3beebac4",
        "description": "Ooyama-kun normally doesn't get involved with Akutsu-san, a delinquent girl in his class, but for some reason she makes his house her hang-out place! Will she do something horrible to him behind closed doors or will he chase her out? But dealing with Akutsu-san's sexy, cute behavior in such a confined space... he\u2019s sure to get flustered! He wants her to go home, but he also doesn't?",
        "cover_url": "https://uploads.mangadex.org/covers/737a846b-2e67-4d63-9f7e-f54b3beebac4/eca1a97a-e53c-4323-b3e7-ce8ccec17451.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "hiatus",
        "tags": [
            "Romance",
            "Comedy",
            "School Life",
            "Delinquents",
            "Slice of Life",
            "Gyaru"
        ],
        "year": 2019,
        "original_language": "ja",
        "manga_id": "737a846b-2e67-4d63-9f7e-f54b3beebac4"
    },
    {
        "title": "Jujutsu Kaisen",
        "url": "/manga/c52b2ce3-7f95-469c-96b0-479524fb7a1a",
        "description": "For some strange reason, Yuji Itadori, despite his insane athleticism would rather just hang out with the Occult Club. However, he soon finds out that the occult is as real as it gets when his fellow club members are attacked!\n\nMeanwhile, the mysterious Megumi Fushiguro is tracking down a special-grade cursed object, and his search leads him to Itadori\u2026\n___\n**Alt Official English:** [VIZ](https://www.viz.com/shonenjump/chapters/jujutsu-kaisen)",
        "cover_url": "https://uploads.mangadex.org/covers/c52b2ce3-7f95-469c-96b0-479524fb7a1a/7dc752c3-8c90-468e-8c75-6903e38d7c7f.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "completed",
        "tags": [
            "Thriller",
            "Monsters",
            "Action",
            "Ghosts",
            "Martial Arts",
            "Magic",
            "Gore",
            "Drama",
            "School Life",
            "Supernatural",
            "Mystery",
            "Tragedy"
        ],
        "year": 2018,
        "original_language": "ja",
        "manga_id": "c52b2ce3-7f95-469c-96b0-479524fb7a1a"
    },
    {
        "title": "Mairimashita! Iruma-kun",
        "url": "/manga/d7037b2a-874a-4360-8a7b-07f2899152fd",
        "description": "Hopeless pushover Iruma Suzuki has found himself in a\u00a0devil\u00a0of a predicament... His trashy parents have sold off his soul, and he now has to live and attend school in the Netherworld. But with his unique survival skills and doting demon grandfather\u2019s support, Iruma will surely make it through this hellish experience. He'll just need to subjugate rival classmates, summon familiars, and more, all while never revealing that he's human... Easy as\u00a0*aleph, bet, gimel*,\u00a0right?",
        "cover_url": "https://uploads.mangadex.org/covers/d7037b2a-874a-4360-8a7b-07f2899152fd/f9927371-1053-4ee3-b68c-713a1182c8a5.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Monsters",
            "Action",
            "Demons",
            "Romance",
            "Comedy",
            "Crossdressing",
            "Magic",
            "Isekai",
            "School Life",
            "Fantasy"
        ],
        "year": 2017,
        "original_language": "ja",
        "manga_id": "d7037b2a-874a-4360-8a7b-07f2899152fd"
    },
    {
        "title": "SPY\u00d7FAMILY",
        "url": "/manga/6b958848-c885-4735-9201-12ee77abcb3c",
        "description": "The master spy codenamed <Twilight> has spent most of his life on undercover missions, all for the dream of a better world. Yet one day he receives a particularly difficult order from command. For his mission, he must form a temporary family and start a new life?! \n\nA Spy/Action/Comedy manga about a one-of-a-kind family!",
        "cover_url": "https://uploads.mangadex.org/covers/6b958848-c885-4735-9201-12ee77abcb3c/11c2207c-6886-43d2-90fd-c765127579c7.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Award Winning",
            "Action",
            "Animals",
            "Romance",
            "Comedy",
            "Martial Arts",
            "Adventure",
            "School Life",
            "Police",
            "Slice of Life",
            "Supernatural"
        ],
        "year": 2019,
        "original_language": "ja",
        "manga_id": "6b958848-c885-4735-9201-12ee77abcb3c"
    },
    {
        "title": "Maou no Ore ga Dorei Elf o Yome ni Shita nda ga, Dou Medereba Ii?",
        "url": "/manga/55ace2fb-e157-4d76-9e72-67c6bd762a39",
        "description": "Zagan is feared as an evil mage, he is awkward and has a sharp tongue, and once again had to put down thieves that encroached on his territory when he was researching that morning. In a dark auction, he finds a white slave elf, Nephie, who holds a peerless beauty. Falling in love with her at first sight, he uses his fortune to buy her, but as poor as he is socially, he doesn\u2019t understand how to connect with her. Thus, the clumsy cohabitation of the mage that can\u2019t convey his love, and the slave that pines for her master but doesn\u2019t understand how to bring it up, begins.",
        "cover_url": "https://uploads.mangadex.org/covers/55ace2fb-e157-4d76-9e72-67c6bd762a39/5d96ae1e-6a04-462d-8134-bb751629db42.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "ongoing",
        "tags": [
            "Action",
            "Demons",
            "Romance",
            "Comedy",
            "Magic",
            "Drama",
            "Fantasy",
            "Monster Girls",
            "Adaptation"
        ],
        "year": 2018,
        "original_language": "ja",
        "manga_id": "55ace2fb-e157-4d76-9e72-67c6bd762a39"
    },
    {
        "title": "Horimiya",
        "url": "/manga/a25e46ec-30f7-4db6-89df-cacbc1d9a900",
        "description": "Kyoko Hori is your average teenage girl\u2026 who has a side she wants no one else to ever discover. Then there's her classmate Izumi Miyamura, your average glasses-wearing boy \u2014 who's also a totally different person outside of school. When the two unexpectedly meet, they discover each other's secrets, and a friendship is born.\n\nRead the official English release on [MangaUp](https://global.manga-up.com/manga/122).",
        "cover_url": "https://uploads.mangadex.org/covers/a25e46ec-30f7-4db6-89df-cacbc1d9a900/04feed00-d919-4c72-b355-15b37555eb1e.jpg.512.jpg",
        "author": "",
        "artist": "",
        "status": "completed",
        "tags": [
            "Romance",
            "Comedy",
            "School Life",
            "Slice of Life",
            "Adaptation"
        ],
        "year": 2011,
        "original_language": "ja",
        "manga_id": "a25e46ec-30f7-4db6-89df-cacbc1d9a900"
    }
]
