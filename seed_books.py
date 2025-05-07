"""
run with: python manage.py shell < seed_books.py
"""

from django.contrib.auth.models import User
from bookMng.models import Book, Rating, Comment, Favorite
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import random
from django.utils import timezone
from decimal import Decimal
from django.db import transaction

# Create placeholder image function
def get_placeholder_image(name="placeholder.png"):
    # Simple 1x1 transparent PNG
    placeholder_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xff\xff?\x03\x00\x08\xfc\x02\xfe\xa7\x9a\xa0\xa0\x00\x00\x00\x00IEND\xaeB`\x82'
    return SimpleUploadedFile(
        name=name,
        content=placeholder_content,
        content_type="image/png"
    )

# Create sample users if they don't exist
users = []
for username in ['admin', 'alice', 'bob', 'charlie', 'david']:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': f'{username}@example.com',
            'is_staff': username == 'admin',
            'is_superuser': username == 'admin',
        }
    )
    if created:
        user.set_password(f'{username}123')
        user.save()
        print(f"Created user: {username}")
    users.append(user)

# Sample book data
book_data = [
    {
        'name': 'Django for Beginners',
        'web': 'https://djangoforbeginners.com',
        'price': Decimal('29.99'),
        'username': users[0],  # admin
    },
    {
        'name': 'Python Crash Course',
        'web': 'https://nostarch.com/pythoncrashcourse2e',
        'price': Decimal('39.95'),
        'username': users[1],  # alice
    },
    {
        'name': 'Clean Code',
        'web': 'https://www.oreilly.com/library/view/clean-code/9780136083238/',
        'price': Decimal('44.99'),
        'username': users[2],  # bob
    },
    {
        'name': 'The Pragmatic Programmer',
        'web': 'https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/',
        'price': Decimal('49.95'),
        'username': users[3],  # charlie
    },
    {
        'name': 'Eloquent JavaScript',
        'web': 'https://eloquentjavascript.net/',
        'price': Decimal('26.99'),
        'username': users[4],  # david
    },
    {
        'name': 'Design Patterns',
        'web': 'https://www.oreilly.com/library/view/design-patterns-elements/0201633612/',
        'price': Decimal('54.99'),
        'username': users[0],  # admin
    },
    {
        'name': 'The Art of Computer Programming',
        'web': 'https://www-cs-faculty.stanford.edu/~knuth/taocp.html',
        'price': Decimal('99.99'),
        'username': users[1],  # alice
    },
    {
        'name': 'Learning React',
        'web': 'https://www.oreilly.com/library/view/learning-react-2nd/9781492051718/',
        'price': Decimal('36.99'),
        'username': users[2],  # bob
    },
    {
        'name': 'JavaScript: The Good Parts',
        'web': 'https://www.oreilly.com/library/view/javascript-the-good/9780596517748/',
        'price': Decimal('29.99'),
        'username': users[3],  # charlie
    },
    {
        'name': 'Algorithms to Live By',
        'web': 'https://algorithmstoliveby.com/',
        'price': Decimal('19.99'),
        'username': users[4],  # david
    }
]

# Create books with transaction to ensure all succeed or none
with transaction.atomic():
    books_created = 0
    books = []

    for i, data in enumerate(book_data):
        # Skip if book already exists
        if Book.objects.filter(name=data['name']).exists():
            print(f"Book '{data['name']}' already exists, skipping.")
            continue

        # Create book
        book = Book(
            name=data['name'],
            web=data['web'],
            price=data['price'],
            username=data['username'],
        )

        # Add placeholder image
        book.picture = get_placeholder_image(f"book_{i}.png")
        book.save()

        # Update pic_path
        book.pic_path = f"uploads/{os.path.basename(book.picture.name)}"
        book.save()

        books.append(book)
        books_created += 1
        print(f"Created book: {book.name}")

    print(f"Successfully created {books_created} books")

    # Optional: Create sample ratings, comments, and favorites
    if books:
        # Add some ratings - MODIFIED to handle the unique constraint
        # Check if we have any existing ratings
        user_with_ratings = set()
        existing_ratings = Rating.objects.all()
        for rating in existing_ratings:
            user_with_ratings.add(rating.user.id)

        print(f"Found {len(user_with_ratings)} users with existing ratings")

        # Only create ratings for users who don't already have one
        available_users = [user for user in users if user.id not in user_with_ratings]

        if available_users:
            # Choose one book to rate per available user
            for user in available_users:
                book = random.choice(books)
                score = random.randint(1, 10)
                Rating.objects.create(
                    book=book,
                    user=user,
                    score=score
                )
                print(f"Added rating of {score} to {book.name} by {user.username}")
        else:
            print("No users available for new ratings")

        # Add some comments
        comments = [
            "Great book! Highly recommended.",
            "This was very helpful for my project.",
            "I learned a lot from this book.",
            "The examples are clear and well-explained.",
            "Could use more detailed explanations.",
            "Perfect for beginners!",
            "A bit too advanced for me.",
            "Excellent reference material.",
            "I refer to this book regularly.",
            "Worth every penny."
        ]

        for book in books:
            for i in range(random.randint(0, 3)):  # 0-3 comments per book
                user = random.choice(users)
                text = random.choice(comments)

                Comment.objects.create(
                    book=book,
                    author=user,
                    text=text,
                    created_date=timezone.now()
                )
                print(f"Added comment to {book.name} by {user.username}")

        # Add some favorites
        for user in users:
            for i in range(random.randint(0, 3)):  # 0-3 favorites per user
                book = random.choice(books)

                # Skip if favorite already exists
                if Favorite.objects.filter(user=user, book=book).exists():
                    continue

                Favorite.objects.create(
                    user=user,
                    book=book
                )
                print(f"Added {book.name} to {user.username}'s favorites")

print("Database seeding complete!")