from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Категорія', max_length=255)
    description = models.TextField('Опис')
    url = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Actor(models.Model):
    name = models.CharField('Ім\'я', max_length=255)
    age = models.PositiveSmallIntegerField('Вік', default=0)
    description = models.TextField('Опис')
    image = models.ImageField('Фото', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автори'
        verbose_name_plural = 'автори'

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={'slug': self.name})


class Genre(models.Model):
    name = models.CharField('Ім\'я', max_length=255)
    description = models.TextField('Опис')
    url = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'


class Movie(models.Model):
    title = models.CharField('Назва', max_length=255)
    tagline = models.CharField('Гасло', max_length=100, default='')
    description = models.TextField('Опис')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Дата виходу', default=2023)
    country = models.CharField('Країна', max_length=255)
    directors = models.ManyToManyField(Actor, verbose_name='Автор', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Співавтор', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='жанри')
    world_premiere = models.DateField('Прем\'єра в світі', default=date.today)
    budget = models.PositiveIntegerField('Ціна', default=0, help_text='in $')
    fees_in_USA = models.PositiveIntegerField('Збори в США', default=0, help_text='in $')
    fees_in_world = models.PositiveIntegerField('Збори в світі', default=0, help_text='in $')
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=255, unique=True)
    draft = models.BooleanField('Чорновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)


    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class MovieShots(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Опис')
    image = models.ImageField('Зображення', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Книга', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фото книги'
        verbose_name_plural = 'Фото книги'


class RatingStar(models.Model):
    value = models.SmallIntegerField('Значення', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Зірка рейтингу'
        verbose_name_plural = 'Зірки рейтингу'
        ordering = ['-value']


class Rating(models.Model):
    ip = models.CharField('ІР адреса', max_length=255)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='зірка')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='книга')

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('Ім\'я', max_length=255)
    text = models.TextField('Коментар', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Батько', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='книга', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
