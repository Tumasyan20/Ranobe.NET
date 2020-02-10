from django.shortcuts import render
from django.contrib.auth.models import User 
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from catalog.models import Chapter, Book, Review, Genre, ChapterComment
from accounts.models import UserProfile

def Book_list(request):
	book_list = Book.objects.all()
	genres = Genre.objects.all()

	tmp = 'light_template.html'

	page = request.GET.get('page', 1)

	paginator = Paginator(book_list, 10)

	try:
		books = paginator.page(page)
	except PageNotAnInteger:
		books = paginator.page(1)
	except EmptyPage:
		books = paginator.page(paginator.num_pages)

	readed_book_count = 0

	if request.user.is_authenticated:

		readed_book_count = UserProfile.objects.get(user_id = request.user.id).readed_books.count()

		profile_theme = UserProfile.objects.get(user_id = request.user.id).theme
		if profile_theme == 'd':
			tmp = 'dark_template.html'
		else:
			tmp = 'light_template.html'

	return render(
		request,
		'catalog/book_list.html',
		context = { 'tmp' 					: tmp, 
					'book_list' 			: book_list, 
					'books' 				: books, 
					'readed_book_count' 	: readed_book_count, 
					'genres' 				: genres,
		}
	)

def book_detail(request, book_id):

	book = Book.objects.filter(id = book_id)
	chapter_list = Chapter.objects.filter(book_id = book_id).all().order_by('-id')
	chapter_a_price = round(chapter_list.aggregate(sum = Sum('price'))['sum']/chapter_list.count())
	lasted_reviews = Review.objects.filter(book_id = book_id).order_by('-pub_date')[:3]
	last_comments = ChapterComment.objects.filter(book_id = book_id)
	tmp = 'light_template.html'

	page = request.GET.get('page', 1)
	paginator = Paginator(chapter_list, 10)
	
	try:
		chapters = paginator.page(page)
	except PageNotAnInteger:
		chapters = paginator.page(1)
	except EmptyPage:
		chapters = paginator.page(paginator.num_pages)

	if request.user.is_authenticated:

		readed_book_count = UserProfile.objects.get(user_id = request.user.id).readed_books.count()

		profile_theme = UserProfile.objects.get(user_id = request.user.id).theme
		if profile_theme == 'd':
			tmp = 'dark_template.html'
		else:
			tmp = 'light_template.html'

	return render(
		request,
		'catalog/book_detail.html',
		context = { 'tmp' 				: tmp, 
					'book' 				: book, 
					'chapters' 			: chapters, 
					'chapter_a_price' 	: chapter_a_price, 
					'lasted_reviews'	: lasted_reviews,
					'last_comments' 	: last_comments,
		}
	)

def chapter_detail(request, chapter_id, book_id):

	chapters = Chapter.objects.filter(book_id = book_id)

	comments = ChapterComment.objects.filter(chapter_id = chapter_id)

	chapter = 0

	index = 0


	for i in chapters:


		if str(i.id) == chapter_id:
			chapter = i
			break

		index += 1


	if index == 0:
		prev_chapter = False
	else:
		prev_chapter = chapters[index - 1]


	if index == len(chapters) - 1:
		next_chapter = False
	else:
		next_chapter = chapters[index + 1]
	

	tmp = 'light_template.html'

	if request.user.is_authenticated:

		readed_book_count = UserProfile.objects.get(user_id = request.user.id).readed_books.count()

		profile_theme = UserProfile.objects.get(user_id = request.user.id).theme

		if profile_theme == 'd':
			tmp = 'dark_template.html'
		else:
			tmp = 'light_template.html'

	return render(
		request,
		'catalog/chapter_detail.html',
		context = {
			'tmp'			: tmp,
			'chapter'		: chapter,
			'prev_chapter'	: prev_chapter,
			'next_chapter'	: next_chapter,
			'comments'		: comments,
		}
	)