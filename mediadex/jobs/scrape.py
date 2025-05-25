from .extensions.batoto import BatoToSource
from .extensions.mangadex import MangaDexSource
from .extensions.demoniscans import MangaDemonSource
from .extensions.interfaces.manga_source import MangaSource


def print_chapter_pages(source: MangaSource, manga_query: str):
    mangas = source.search(manga_query)
    if not mangas:
        print("Aucun manga trouvé")
        return
    manga = mangas[0]
    print(f"Manga trouvé : {manga['title']}")

    chapters = source.get_chapters(manga['url'])
    if not chapters:
        print("Aucun chapitre trouvé")
        return
    chapter = chapters[0]
    print(f"Premier chapitre : {chapter['title']}")

    pages = source.get_pages(chapter['url'])
    print("Pages du chapitre:")
    for page in pages:
        print(page)




if __name__ == '__main__':
    # source_name = input('Choose source name: ')
    source_name = 'batoto'
    source = None
    
    if source_name == 'batoto':
        source = BatoToSource()
    if source_name == 'mangadex':
        source = MangaDexSource()
    if source_name == 'demonics':
        source = MangaDemonSource()
        
    if source:
        print_chapter_pages(source, "One Piece official")
