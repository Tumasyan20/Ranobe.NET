from django.contrib import admin

from .models import Book, Genre, Country, Author, Chapter, ChapterComment, Review


admin.site.register(Review)
admin.site.register(Author)
admin.site.register(Country)
admin.site.register(Genre)


class ChapterInline(admin.TabularInline):
	model = Chapter
	extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'country', 'publisher',)
	fields = ['title', 'summary', 'author', 'book_rating', 'country', 'image' ,'publisher', 'genre', 'pub_date', 'last_pub_date']
	readonly_fields = ('pub_date',)
	inlines = [ChapterInline]

class ChapterCommentInline(admin.TabularInline):
	model = ChapterComment
	extra = 1

@admin.register(ChapterComment)
class ChapterCommentAdmin(admin.ModelAdmin):
	list_display = ('book', 'chapter', 'commentator', 'pub_date')

@admin.register(Chapter)
class Chapter(admin.ModelAdmin):
	list_display = ('book', 'title', 'number', 'pub_date')	
	list_filter = ('book', 'pub_date')
	inlines = [ChapterCommentInline]
