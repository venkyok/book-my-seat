"""
Demo data for Vercel deployment (SQLite read-only mode)
This provides hardcoded data to showcase the application without database writes
"""

from datetime import datetime, timedelta
from django.utils import timezone

# Demo Movies Data
DEMO_MOVIES = [
    {
        'id': 1,
        'name': 'The Shawshank Redemption',
        'genre': 'Drama',
        'language': 'English',
        'poster': 'https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=6hB3S9bIaco',
        'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.'
    },
    {
        'id': 2,
        'name': 'The Dark Knight',
        'genre': 'Action',
        'language': 'English',
        'poster': 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=EXeTwQWrcwY',
        'description': 'When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest psychological and physical tests.'
    },
    {
        'id': 3,
        'name': 'Inception',
        'genre': 'Sci-Fi',
        'language': 'English',
        'poster': 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=YoHD9XEInc0',
        'description': 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.'
    },
    {
        'id': 4,
        'name': 'RRR',
        'genre': 'Action',
        'language': 'Telugu',
        'poster': 'https://m.media-amazon.com/images/M/MV5BODUwNDNjYzctODUxNy00ZTA2LWIyYTEtMDc5Y2E5ZjBmNTMzXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_SX300.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=f_vbAtFSEc0',
        'description': 'A fictional story about two legendary revolutionaries and their journey away from home before they started fighting for their country.'
    },
    {
        'id': 5,
        'name': 'Interstellar',
        'genre': 'Sci-Fi',
        'language': 'English',
        'poster': 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=zSWdZVtXT7E',
        'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.'
    },
    {
        'id': 6,
        'name': '3 Idiots',
        'genre': 'Comedy',
        'language': 'Hindi',
        'poster': 'https://m.media-amazon.com/images/M/MV5BNTkyOGVjMGEtNmQzZi00NzFlLTlhOWQtODYyMDc2ZGJmYzFhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=K0eDlFX9GMc',
        'description': 'Two friends are searching for their long lost companion. They revisit their college days and recall the memories of their friend.'
    },
    {
        'id': 7,
        'name': 'Avengers: Endgame',
        'genre': 'Action',
        'language': 'English',
        'poster': 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=TcMBFSGVi1c',
        'description': 'After Thanos\' snap, the Avengers gather once more to reverse the Mad Titan\'s actions and restore balance to the universe.'
    },
    {
        'id': 8,
        'name': 'Parasite',
        'genre': 'Thriller',
        'language': 'Korean',
        'poster': 'https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_SX300.jpg',
        'trailer_url': 'https://www.youtube.com/watch?v=5xH0HfJHsaY',
        'description': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.'
    },
]

# Demo Theaters Data
DEMO_THEATERS = {
    1: [  # The Shawshank Redemption
        {'id': 1, 'name': 'PVR Phoenix', 'show_time': '10:00 AM', 'price': 250, 'total_seats': 50, 'booked_seats': 15},
        {'id': 2, 'name': 'INOX Forum', 'show_time': '2:30 PM', 'price': 300, 'total_seats': 60, 'booked_seats': 22},
        {'id': 3, 'name': 'Cinepolis Mall', 'show_time': '6:45 PM', 'price': 280, 'total_seats': 55, 'booked_seats': 18},
    ],
    2: [  # The Dark Knight
        {'id': 4, 'name': 'PVR Phoenix', 'show_time': '11:30 AM', 'price': 350, 'total_seats': 70, 'booked_seats': 35},
        {'id': 5, 'name': 'INOX Forum', 'show_time': '4:00 PM', 'price': 400, 'total_seats': 65, 'booked_seats': 40},
        {'id': 6, 'name': 'Cinepolis Mall', 'show_time': '9:00 PM', 'price': 380, 'total_seats': 68, 'booked_seats': 50},
    ],
    3: [  # Inception
        {'id': 7, 'name': 'PVR Phoenix', 'show_time': '1:00 PM', 'price': 320, 'total_seats': 58, 'booked_seats': 25},
        {'id': 8, 'name': 'INOX Forum', 'show_time': '5:30 PM', 'price': 350, 'total_seats': 62, 'booked_seats': 30},
        {'id': 9, 'name': 'Cinepolis Mall', 'show_time': '10:15 PM', 'price': 340, 'total_seats': 60, 'booked_seats': 28},
    ],
    4: [  # RRR
        {'id': 10, 'name': 'PVR Phoenix', 'show_time': '12:00 PM', 'price': 300, 'total_seats': 80, 'booked_seats': 60},
        {'id': 11, 'name': 'INOX Forum', 'show_time': '3:30 PM', 'price': 280, 'total_seats': 75, 'booked_seats': 55},
        {'id': 12, 'name': 'Cinepolis Mall', 'show_time': '7:00 PM', 'price': 290, 'total_seats': 78, 'booked_seats': 58},
    ],
    5: [  # Interstellar
        {'id': 13, 'name': 'PVR Phoenix', 'show_time': '2:00 PM', 'price': 330, 'total_seats': 65, 'booked_seats': 20},
        {'id': 14, 'name': 'INOX Forum', 'show_time': '6:00 PM', 'price': 360, 'total_seats': 70, 'booked_seats': 25},
        {'id': 15, 'name': 'Cinepolis Mall', 'show_time': '10:30 PM', 'price': 350, 'total_seats': 68, 'booked_seats': 22},
    ],
    6: [  # 3 Idiots
        {'id': 16, 'name': 'PVR Phoenix', 'show_time': '11:00 AM', 'price': 250, 'total_seats': 72, 'booked_seats': 45},
        {'id': 17, 'name': 'INOX Forum', 'show_time': '3:00 PM', 'price': 270, 'total_seats': 68, 'booked_seats': 42},
        {'id': 18, 'name': 'Cinepolis Mall', 'show_time': '8:00 PM', 'price': 260, 'total_seats': 70, 'booked_seats': 48},
    ],
    7: [  # Avengers: Endgame
        {'id': 19, 'name': 'PVR Phoenix', 'show_time': '10:30 AM', 'price': 400, 'total_seats': 85, 'booked_seats': 70},
        {'id': 20, 'name': 'INOX Forum', 'show_time': '2:00 PM', 'price': 450, 'total_seats': 80, 'booked_seats': 68},
        {'id': 21, 'name': 'Cinepolis Mall', 'show_time': '6:30 PM', 'price': 420, 'total_seats': 82, 'booked_seats': 72},
    ],
    8: [  # Parasite
        {'id': 22, 'name': 'PVR Phoenix', 'show_time': '1:30 PM', 'price': 310, 'total_seats': 52, 'booked_seats': 18},
        {'id': 23, 'name': 'INOX Forum', 'show_time': '5:00 PM', 'price': 340, 'total_seats': 55, 'booked_seats': 20},
        {'id': 24, 'name': 'Cinepolis Mall', 'show_time': '9:30 PM', 'price': 330, 'total_seats': 53, 'booked_seats': 19},
    ],
}

# Demo Seats Data (for seat selection page)
def generate_demo_seats(theater_id, total_seats, booked_count):
    """Generate demo seats for a theater"""
    seats = []
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    seats_per_row = total_seats // len(rows)
    
    seat_number = 1
    booked_so_far = 0
    
    for row in rows:
        for col in range(1, seats_per_row + 1):
            is_booked = booked_so_far < booked_count and (seat_number % 3 == 0 or seat_number % 5 == 0)
            if is_booked:
                booked_so_far += 1
            
            seats.append({
                'id': seat_number,
                'seat_number': f'{row}{col}',
                'row': row,
                'is_booked': is_booked,
                'theater_id': theater_id
            })
            seat_number += 1
    
    return seats

# Genre and Language choices
GENRE_CHOICES = [
    ('Action', 'Action'),
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Horror', 'Horror'),
    ('Romance', 'Romance'),
    ('Sci-Fi', 'Sci-Fi'),
    ('Thriller', 'Thriller'),
]

LANGUAGE_CHOICES = [
    ('English', 'English'),
    ('Hindi', 'Hindi'),
    ('Telugu', 'Telugu'),
    ('Tamil', 'Tamil'),
    ('Malayalam', 'Malayalam'),
    ('Kannada', 'Kannada'),
    ('Korean', 'Korean'),
]


class DemoMovie:
    """Mock Movie object for demo mode"""
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.language = data['language']
        self.poster = data.get('poster', '')
        self.trailer_url = data.get('trailer_url', '')
        self.description = data.get('description', '')
        
    def __str__(self):
        return self.name
        
    GENRE_CHOICES = GENRE_CHOICES
    LANGUAGE_CHOICES = LANGUAGE_CHOICES


class DemoTheater:
    """Mock Theater object for demo mode"""
    def __init__(self, data, movie):
        self.id = data['id']
        self.name = data['name']
        self.show_time = data['show_time']
        self.price = data['price']
        self.total_seats = data.get('total_seats', 60)
        self.booked_seats = data.get('booked_seats', 0)
        self.movie = movie
        
    def __str__(self):
        return f"{self.name} - {self.show_time}"
        
    @property
    def available_seats(self):
        return self.total_seats - self.booked_seats


class DemoSeat:
    """Mock Seat object for demo mode"""
    def __init__(self, data):
        self.id = data['id']
        self.seat_number = data['seat_number']
        self.row = data['row']
        self.is_booked = data['is_booked']
        self.theater_id = data['theater_id']
        self.reserved_by = None
        self.reserved_until = None
        
    def __str__(self):
        return self.seat_number


def get_demo_movies(search=None, genre=None, language=None):
    """Get filtered demo movies"""
    movies = [DemoMovie(m) for m in DEMO_MOVIES]
    
    if search:
        movies = [m for m in movies if search.lower() in m.name.lower()]
    
    if genre:
        movies = [m for m in movies if m.genre == genre]
    
    if language:
        movies = [m for m in movies if m.language == language]
    
    return movies


def get_demo_movie(movie_id):
    """Get a single demo movie by ID"""
    for movie_data in DEMO_MOVIES:
        if movie_data['id'] == int(movie_id):
            return DemoMovie(movie_data)
    return None


def get_demo_theaters(movie_id):
    """Get demo theaters for a movie"""
    movie = get_demo_movie(movie_id)
    if not movie:
        return []
    
    theater_list = DEMO_THEATERS.get(int(movie_id), [])
    return [DemoTheater(t, movie) for t in theater_list]


def get_demo_theater(theater_id):
    """Get a single demo theater by ID"""
    for movie_id, theaters in DEMO_THEATERS.items():
        for theater_data in theaters:
            if theater_data['id'] == int(theater_id):
                movie = get_demo_movie(movie_id)
                return DemoTheater(theater_data, movie)
    return None


def get_demo_seats(theater_id):
    """Get demo seats for a theater"""
    theater = get_demo_theater(theater_id)
    if not theater:
        return []
    
    seat_data = generate_demo_seats(
        theater_id, 
        theater.total_seats, 
        theater.booked_seats
    )
    return [DemoSeat(s) for s in seat_data]
