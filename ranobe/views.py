from django.shortcuts import render
from django.contrib.auth.models import User 
from catalog.models import Chapter, Book, Review
from accounts.models import UserProfile

from django.contrib.auth.models import Permission

def index(request):
	last_updated_top_books = Book.objects.order_by('-last_pub_date').order_by('-book_rating')[:4]
	top_books = Book.objects.order_by('-book_rating')[:10]
	lasted_reviews = Review.objects.order_by('-pub_date')[:5]
	last_updated_books = Book.objects.order_by('-last_pub_date')[:20]

	readed_book_count = 0

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
		'index.html',
		context = { 'last_updated_top_books' 	: last_updated_top_books, 
					'top_books' 				: top_books, 
					'lasted_reviews' 			: lasted_reviews, 
					'tmp' 						: tmp, 
					'readed_book_count' 		: readed_book_count, 
					'last_updated_books' 		: last_updated_books,
		}
	)