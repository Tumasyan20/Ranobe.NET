from django.db import models
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse 
from django.utils import timezone

import datetime

# Create your models here.

class Chapter(models.Model):

	book = models.ForeignKey("Book", on_delete = models.CASCADE)
	title = models.CharField('Навзание', max_length = 100)
	price = models.IntegerField('Цена', validators = [MinValueValidator(0)], default = 0)
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	content = models.TextField('Содержание главы', default = 'Содержание главы...')
	number = models.IntegerField('Номер главы', validators = [MinValueValidator(1)], null = True, blank = True)
	pay_users = models.ManyToManyField(User, blank = True, help_text = 'Пользователи, что купили данную главу')


	AVAILABILITY_STATUS = (
		('f', 'Бесплатный'),
		('p', 'Платный'),
	)

	status = models.CharField('Статус', max_length = 1, choices = AVAILABILITY_STATUS, default = 'f', help_text = 'Статус главы')

	class Meta:
		verbose_name = 'Глава'
		verbose_name_plural = 'Главы'

	def get_absolute_url(self):
		return reverse('chapter-detail', args = [str(self.book.id), str(self.id)])

	def was_published_recently(self):
		return self.pub_date >= (timezone.now() - datetime.timedelta(days = 3))

	def __str__(self):
		return '%s ( %s )' % (self.title, self.book)


class Genre(models.Model):

	name = models.CharField('Название', max_length = 100, help_text = 'Введите название жанра.')

	class Meta:
		verbose_name = 'Жанр'
		verbose_name_plural = 'Жанры'

	def get_absolute_url(self):
		return reverse('genre-detail', args = [str(self.id)])

	def __str__ (self):
		return self.name


class Country(models.Model):

	name = models.CharField('Страна', max_length = 100, help_text = 'Введите название страны.')

	class Meta:
		verbose_name = 'Страна'
		verbose_name_plural = 'Страны'

	def get_absolute_url(self):
		return reverse('country-detail', args = [str(self.id)])

	def __str__ (self):
		return self.name


class Author(models.Model):

	nickname = models.CharField('Никнейм', max_length = 100)

	class Meta:
		verbose_name = 'Автор'
		verbose_name_plural = 'Авторы'

	class Meta:
		verbose_name = 'Автор'

	def get_absolute_url(self):
		return reverse('author-detail', args = [str(self.id)])

	def __str__ (self):
		return self.nickname


class ChapterComment(models.Model):
	book = models.ForeignKey('Book', on_delete = models.CASCADE, verbose_name = 'Книга')
	commentator = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
	chapter = models.ForeignKey('Chapter', verbose_name = 'Глава', on_delete = models.CASCADE)
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	content = models.TextField('Содержание кометария', max_length = 500)

	class Meta:
		verbose_name = 'Комментарий к главе'
		verbose_name_plural = 'Комментарии к главам'

	def __str__(self):
		return self.content

class Review(models.Model):

	author = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
	title = models.CharField('Навзание рецензии', max_length = 100)
	content = models.TextField('Содержание рецензии')
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	rating = models.IntegerField('Оценка', validators = [MinValueValidator(0), MaxValueValidator(5)], help_text = 'Оценка пользователья к данной книге ( 1 - 5)')
	book = models.ForeignKey('Book', on_delete = models.CASCADE)

	class Meta:
		verbose_name = 'Резенция'
		verbose_name_plural = 'Резенции'

	def get_absolute_url(self):
		return reverse('review-detail', args = [str(self.id)])

	def __str__(self):
		return '%s ( %s )' % (self.title, self.author)


class Book(models.Model):

	title = models.CharField('Название', max_length = 100)
	author = models.ForeignKey(Author, verbose_name = 'Автор', on_delete = models.CASCADE, null = True)
	summary = models.TextField('Описание', max_length = 500, help_text = 'Краткое описание данной книги.')
	genre = models.ManyToManyField(Genre, help_text = 'Жанры данной книги.')
	country = models.ForeignKey(Country, on_delete = models.SET_NULL, null = True)
	pub_date = models.DateTimeField('Дата публикации', auto_now_add = True)
	publisher = models.ForeignKey(User, on_delete = models.CASCADE)
	book_rating = models.IntegerField('Средняя оценка данной книги', default = 0)
	image = models.ImageField('Изображение книги', upload_to = 'images/books', null = True, blank = True)
	last_pub_date = models.DateTimeField('Дата публикации последней главы', null = True, blank = True)

	@receiver(post_save, sender = Chapter)
	def update_last_pub_date(sender, instance, **kwargs):
		chapter_book = Book.objects.get(id = instance.book_id)
		chapter_book.last_pub_date = instance.pub_date
		chapter_book.save()

	@receiver(post_save, sender = Review)
	def update_book_rating(sender, instance, **kwargs):
		update_book = Book.objects.get(id = instance.book_id)
		all_review_count_for_this_book = Review.objects.filter(book_id = instance.book_id).count()
		book_reviews_rating_sum = Review.objects.filter(book_id = instance.book_id).aggregate(sum = Sum('rating'))
		update_book.book_rating = book_reviews_rating_sum['sum']/all_review_count_for_this_book
		update_book.save()

	class Meta:
		verbose_name = 'Книга'
		verbose_name_plural = 'Книги'

	def __str__ (self):
		return self.title

	def get_absolute_url(self):
		return reverse('book-detail', args = [str(self.id)])

	def get_last_chapter(self):
		get_chapters = Chapter.objects.filter(book_id = self.id).all()
		get_last_chapter = get_chapters.order_by('-pub_date')[:1]
		
		return get_last_chapter