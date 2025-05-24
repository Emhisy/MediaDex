from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField()
    
    def __str__(self):
        return self.text

# Manga
    
class Manga(models.Model):
    name = models.CharField()
    description = models.TextField(default='')
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.name
    
class MangaChapter(models.Model):
    name = models.CharField()
    number = models.IntegerField(default=1)
    chapter = models.ForeignKey(Manga, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return f"chapter {self.number}: {self.name}"

class MangaChapterPage(models.Model):
    number = models.IntegerField(default=1)
    file = models.FileField(default=None)
    chapter = models.ForeignKey(MangaChapter, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.number

class MangaTag(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, default=None)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, default=None)

class MangaComment(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, default=None)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, default=None)

# Novel

class Novel(models.Model):
    name = models.CharField()
    description = models.TextField(default='')
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.name

class NovelChapter(models.Model):
    name = models.CharField()
    number = models.IntegerField(default=1)
    text = models.TextField(default='')
    chapter = models.ForeignKey(Novel, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return f"chapter {self.number}: {self.name}"

class NovelTag(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, default=None)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, default=None)

class NovelComment(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, default=None)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, default=None)
