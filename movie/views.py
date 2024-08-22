from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from .models import Movie
# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request,'home.html', {'name':'Juan Velasquez'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_view(request):
    matplotlib.use('Agg')
    
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        movie_counts_by_year[year] = movies_in_year.count()

    
    movie_counts_by_genre = {}
    all_movies = Movie.objects.all()

    for movie in all_movies:
        
        if movie.genre:
            first_genre = movie.genre.split(',')[0].strip() 
        else:
            first_genre = "None" 

        if first_genre in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] += 1
        else:
            movie_counts_by_genre[first_genre] = 1

    bar_width = 0.5
    bar_positions_years = range(len(movie_counts_by_year))

    plt.figure(figsize=(10, 5))
    plt.bar(bar_positions_years, movie_counts_by_year.values(), width=bar_width, align="center")
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions_years, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer_years = io.BytesIO()
    plt.savefig(buffer_years, format='png')
    buffer_years.seek(0)
    plt.close()

    image_png_years = buffer_years.getvalue()
    buffer_years.close()
    graphic_years = base64.b64encode(image_png_years).decode('utf-8')

    
    bar_positions_genres = range(len(movie_counts_by_genre))

    plt.figure(figsize=(10, 5))
    plt.bar(bar_positions_genres, movie_counts_by_genre.values(), width=bar_width, align="center")
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions_genres, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer_genres = io.BytesIO()
    plt.savefig(buffer_genres, format='png')
    buffer_genres.seek(0)
    plt.close()

    image_png_genres = buffer_genres.getvalue()
    buffer_genres.close()
    graphic_genres = base64.b64encode(image_png_genres).decode('utf-8')

    
    return render(request, 'statistics.html', {
        'graphic_years': graphic_years,
        'graphic_genres': graphic_genres
    })
