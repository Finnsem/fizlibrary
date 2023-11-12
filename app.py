from sqlite3 import IntegrityError
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Book, User, SearchForm
from flask_migrate import Migrate
from datetime import timedelta
from flask_caching import Cache
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.permanent_session_lifetime = timedelta(minutes=5)
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s [%(levelname)s] - %(message)s')

# Assuming DevelopmentConfig is defined in config.py with the necessary settings
app.config.from_object('config.DevelopmentConfig')
migrate = Migrate(app, db)

# Initialize the database with the Flask app
db.init_app(app)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@app.route('/clear_cache')
def clear_cache():
    cache.clear()
    return 'Cache has been cleared'



@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif session.get('role') != 'librarian':  # Check if the logged-in user is not a librarian
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('login'))  # Redirect to login if not a librarian
    else:
        books = Book.query.all()
        return render_template('index.html', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        session.permanent = True
        if user and check_password_hash(user.password_hash, password):
            if role == 'user' and user.role == 'user':
                # User's credentials are correct and role is user
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = 'user'
                flash('You were successfully logged in as a user', 'success')
                return redirect(url_for('view_books'))  # Redirect users to the book viewing page
            elif role == 'librarian' and user.role == 'librarian':
                # User's credentials are correct and role is librarian
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = 'librarian'
                flash('You were successfully logged in as a librarian', 'success')
                return redirect(url_for('index'))  # Librarian has access to dashboard
            else:
                # The user's role does not match or credentials are wrong
                flash('Invalid role or credentials', 'danger')
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')



@app.route('/view_books')
def view_books():
    if not session.get('logged_in') or session.get('role') != 'user':
        flash('You do not have permission to view this page', 'danger')
        return redirect(url_for('login'))

    # Assuming you have a Book model with books data
    books = Book.query.all()  # Fetch all books from the database

    return render_template('view.html', books=books)





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')  # Get the role from the form

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user instance with the role
        new_user = User(username=username, email=email, password_hash=hashed_password, role=role)

        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully, please login.')
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            flash('Username or email already exists.')
            logging.error(f'IntegrityError: {str(e)} - Request data: {request.form.to_dict()}')
            return "<script>handleIntegrityError();</script>"

    return render_template('register.html')

from flask import session, redirect, url_for, flash, render_template, request

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    # Check if user is logged in and is a librarian
    if 'logged_in' in session and session['role'] == 'librarian':
        if request.method == 'POST':
            # Get form data
            entry_number = request.form['entry_number']
            title = request.form['title']
            author = request.form['author']
            publisher = request.form['publisher']
            isbn = request.form['isbn']
            version = request.form['version']
            shelf = request.form['shelf']
            
            # Create a new Book instance
            new_book = Book(
                entry_number=entry_number,
                title=title,
                author=author,
                publisher=publisher,
                isbn=isbn,
                version=version,
                shelf=shelf
            )
            
            # Add to the database session and commit
            db.session.add(new_book)
            try:
                db.session.commit()
                flash('Book added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Error adding book: ' + str(e), 'danger')
            
            # Redirect to the book addition page or somewhere else
            return redirect(url_for('add_book'))

        return render_template('add_book.html')
    else:
        # If user is not logged in or not a librarian, deny access
        flash('Access denied: You must be a librarian to access this page.', 'danger')
        return redirect(url_for('login'))  # Redirect to login page


@app.route('/book/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        # Get form data
        book.entry_number = request.form['entry_number']
        book.title = request.form['title']
        book.author = request.form['author']
        book.publisher = request.form['publisher']
        book.isbn = request.form['isbn']
        book.version = request.form['version']
        book.shelf = request.form['shelf']

        try:
            db.session.commit()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('index'))  # Redirect to the book list or detail view
        except Exception as e:
            db.session.rollback()
            flash('Error updating book: ' + str(e), 'danger')
    
    return render_template('update_book.html', book=book)


@app.route('/book/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Attempt to retrieve the book; handle cases where the book does not exist
    book = Book.query.get(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('index'))

    # Delete the book and handle any potential database exceptions
    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully.', 'success')
    except Exception as e:
        # Log the exception for debugging
        print("Error deleting book: ", e)
        db.session.rollback()
        flash('Error deleting book.', 'error')

    # Redirect to the index page after deletion
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Remove user information from the session
    session.clear()
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Check if the user is logged in and has the correct role
    if session.get('logged_in') and session.get('role') == 'librarian':
        search_form = SearchForm()
        if search_form.validate_on_submit():
            query = search_form.query.data
            books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
            return render_template('search_results.html', books=books, query=query)
        return render_template('search.html', form=search_form)
    else:
        flash('Unauthorized access. Please log in as a librarian.', 'danger')
        return redirect(url_for('login'))
    

#add user funct
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if session.get('role') == 'librarian':
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')  # Get the role from the form

            # Hash the password
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            # Create a new user instance
            new_user = User(username=username, email=email, password_hash=hashed_password, role=role)

            # Add the new user to the database
            db.session.add(new_user)
            try:
                db.session.commit()
                flash('New user added successfully.', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Username or email already exists.', 'danger')
            
            return redirect(url_for('add_user'))

        return render_template('add_user.html')
    else:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('view_users'))

@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    if session.get('role') == 'librarian':
        user = User.query.get_or_404(user_id)
        if request.method == 'POST':
            user.username = request.form.get('username', user.username)
            user.email = request.form.get('email', user.email)
            password = request.form.get('password')
            if password:
                user.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            user.role = request.form.get('role', user.role)

            db.session.commit()
            flash('User updated successfully', 'success')
            return redirect(url_for('view_users'))  # Replace with your desired redirect

        return render_template('update_user.html', user=user)
    else:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
@app.route('/view_users')
def view_users():
    if session.get('role') == 'librarian':
        all_users = User.query.all()
        return render_template('view_users.html', users=all_users)
    else:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if session.get('role') == 'librarian':
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', 'success')
        return redirect(url_for('view_users'))
    else:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    


# Initialize the database tables, if they don't already exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
