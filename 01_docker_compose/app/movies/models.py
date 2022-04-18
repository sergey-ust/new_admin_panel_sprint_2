"""ORM models for film work application."""

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

_PERSON_NAME_MAX_LEN = 200
_FILM_NAME_MAX_LEN = 200
_FILM_TYPE_NAME_MAX_LEN = 15
_ROLE_MAX_LEN = 15


class TimeStampedMixin(models.Model):
    """Base class for models with created/modified timestamps."""

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Base class for models with Django generated UUID(Primary key)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_(_('genre_name')), max_length=100, unique=True)
    description = models.TextField(_('description'), null=True, blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self) -> str:
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('name'), max_length=_PERSON_NAME_MAX_LEN)

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self) -> str:
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    class _FilmType(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')
        __empty__ = _('(unknown)')

    title = models.CharField(_('film_name'), max_length=_FILM_NAME_MAX_LEN)
    description = models.TextField(_('description'))
    creation_date = models.DateField(_('creation date'))
    rating = models.FloatField(
        _('rating'),
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100.0)],
    )
    type = models.CharField(
        _('type'),
        max_length=_FILM_TYPE_NAME_MAX_LEN,
        choices=_FilmType.choices,
        default=_FilmType.MOVIE,
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    person = models.ManyToManyField(Person, through='PersonFilmWork')

    # If DB should check a field value, add "models.CheckConstraint" in "Meta"
    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _('film work')
        verbose_name_plural = _('film works')

    def __str__(self) -> str:
        return self.title + ' ({0})'.format(self.creation_date.year)


class GenreFilmWork(UUIDMixin):
    """Many To Many for "FilmWork" and "Genre"."""

    film_work = models.ForeignKey(
        'FilmWork', on_delete=models.CASCADE, verbose_name=_('film work'),
        db_index=False
    )
    genre = models.ForeignKey(
        'Genre', on_delete=models.CASCADE, verbose_name=_('genre'),
        db_index=False
    )
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _('film genre')
        verbose_name_plural = _('film genres')
        constraints = [
            models.UniqueConstraint(fields=('film_work', 'genre'),
                                    name='unique_film_genre')
        ]
        indexes = [
            models.Index(
                fields=['film_work'],
                name='genre_film_work_film_work_id'
            ),
            models.Index(
                fields=['genre'],
                name='genre_film_work_genre_id'
            ),
        ]

    def __str__(self) -> str:
        """No printable information."""
        return ''


class PersonFilmWork(UUIDMixin):
    """Many To Many for "FilmWork" and "Person"."""

    class Role(models.TextChoices):
        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')
        WRITER = 'writer', _('writer')
        __empty__ = _('(unknown)')

    film_work = models.ForeignKey(
        'FilmWork', on_delete=models.CASCADE, verbose_name=_('film work'),
        db_index=False
    )
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, verbose_name=_('person'),
        db_index=False
    )
    role = models.CharField(
        _('role'),
        max_length=_ROLE_MAX_LEN,
        choices=Role.choices,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _('film person')
        verbose_name_plural = _('film persons')
        indexes = [
            models.Index(
                fields=['film_work'],
                name='person_film_work_film_work_id'
            ),
            models.Index(
                fields=['person'],
                name='person_film_work_person_id'
            ),
        ]

    def __str__(self) -> str:
        return ''
