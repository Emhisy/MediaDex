from django.contrib import admin
from .models import \
    Manga, MangaChapter, MangaChapterPage, MangaComment, \
    Novel, NovelChapter, NovelComment, \
    Tag, Comment


class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]
    list_display = ['name']

class TagInline(admin.TabularInline):
    model = Tag
    fields = ['name'] 
    extra = 1
    
class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['text']}),
    ]
    list_display = ['text']

admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
    
# Manga

class MangaTagInline(admin.TabularInline):
    model = Manga.tags.through
    extra = 1
    
class MangaChapterInline(admin.TabularInline):
    model = MangaChapter
    extra = 1
    
class MangaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['description']}),
    ]
    inlines = [MangaTagInline, MangaChapterInline]
    list_display = ('name', 'description', 'get_tags')
    
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    
    get_tags.short_description = 'Tags'

class MangaChapterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['number']}),
        (None,               {'fields': ['chapter']}),
    ]
    list_display = ('name', 'number', 'chapter')

class MangaChapterPageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['number']}),
        (None,               {'fields': ['file']}),
        (None,               {'fields': ['chapter']}),
    ]
    list_display = ('number', 'file', 'chapter')
    
class MangaCommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['manga']}),
        (None,               {'fields': ['comment']}),
    ]
    list_display = ('manga', 'comment')

admin.site.register(Manga, MangaAdmin)
admin.site.register(MangaChapter, MangaChapterAdmin)
admin.site.register(MangaChapterPage, MangaChapterPageAdmin)
admin.site.register(MangaComment, MangaCommentAdmin)

# Novel

class NovelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_tags')
    
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    
    get_tags.short_description = 'Tags'

class NovelChapterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['number']}),
        (None,               {'fields': ['text']}),
    ]
    list_display = ('name', 'number', 'text')
    
class NovelCommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['novel']}),
        (None,               {'fields': ['comment']}),
    ]
    list_display = ('novel', 'comment')
    
admin.site.register(Novel, NovelAdmin)
admin.site.register(NovelChapter, NovelChapterAdmin)
admin.site.register(NovelComment, NovelCommentAdmin)
