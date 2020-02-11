from django.db import models
from catalog.models import Book
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	avatar = models.ImageField(upload_to = 'images/users', verbose_name = 'Изображение', default = 'images/users/noavatar.png')
	balacne = models.IntegerField('Баланс', validators = [MinValueValidator(0)], default = 0)

	THEME_VARIANTS = (
		('l', 'Светлый'),
		('d', 'Темный'),
	)

	theme = models.CharField('Тема', max_length = 1, choices = THEME_VARIANTS, default = 'l', help_text = 'Тема страницы, для пользователья.')
	readed_books = models.ManyToManyField(Book, verbose_name = 'Книги, отмеченные как - "Прочитано"', blank = True)

	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('user-detail', args = [str(self.user.id)])


	@receiver(post_save, sender = User)
	def update_userprofile(instance, created, **kwargs):
		if created:
			#profile = UserProfile.objects.get()
			UserProfile.objects.create(user = instance)

	def __unicode__(self):
		return self.user

	class Meta:
		verbose_name = 'Профиль'
		verbose_name_plural = 'Профили'

