from django.db import models

class Profile(models.Model):
    username = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.username

class Author(models.Model):
    name = models.CharField(max_length=100)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name='published_books')
    release_date = models.DateField()

    def __str__(self):
        return self.title


class Reviewer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.reviewer.name}'s review of {self.book.title}"


class Store(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='stores')

    def __str__(self):
        return self.name
