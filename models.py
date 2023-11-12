<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard | Library Management System</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    <style>
        body, button, input, select, textarea {
            font-family: 'Roboto', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #AFBC88;
            color: #333;
            line-height: 2;
        }

        .sidebar {
            height: 100vh;
            width: 250px;
            position: fixed;
            background-color: #333;
            padding-top: 20px;
        }

        .sidebar a {
            padding: 10px 15px;
            text-decoration: none;
            font-size: 1.1em;
            color: #afbc88;
            display: block;
        }

        .sidebar a:hover {
            background: #575757;
            transform: scale(1.1);
            transition: all .2s ease-in-out;
            border-radius: 5px;
            margin-left: 30px;
        }

        .content {
            margin-left: 250px;
            
            text-align: center;
        }

        .header {
            padding: 10px 0;
            background-color: #40531b;
            color: white;
            text-align: center;
        }

        .books-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 3fr));
            gap: 0.2rem;
        }

        .book-card {

            width: 250px;
            margin: 10px;
            margin-left: 30px;
            padding: 40px 30px;
            background: #90b979;
            border-radius: 10px;
            box-shadow: -6px -6px 20px rgba(255, 255, 255, 0.295),6px 6px 20px rgba(0,0,0,0.1);
        }

        .book-card:hover {
            background: #476636;
            transform: scale(1.1);
            transition: all .2s ease-in-out;
            box-shadow: inset -6px -6px 20px rgba(35, 150, 73, 0.5),inset 6px 6px 20px rgba(0,0,0,0.05);
        }

        .book-title {
            font-size: 1.3em;
            line-height: normal;
            color: #f7f7f7;
            margin: 0;
        }

        .book-author {
            color: #f8f8f8;
            font-size: 0.9em;
           
        }

        .btn {
            display: inline-block;
            border: none;
            margin-top: 10px;
            padding-left: 20px;
            padding-top: 10px;
            padding-bottom: 10px;
            padding-right: 20px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .update-btn {
            background-color: #4cd137;
            color: #fff;
            text-decoration: none;
        }

        .delete-btn {
            background-color: #ff6b6b;
            color: #fff;
            margin-left: 10px;
        }

        .update-btn:hover {
            background-color: #43a047;
        }

        

        @media (max-width: 960px) {
            .sidebar {
                width: 100%;
                height: auto;
                position: relative;
            }

            .content {
                margin-left: 0;
            }

            .books-container {
                grid-template-columns: 1fr;
            }

            .books-container:hover {
                grid-template-columns: 1fr;
                transform: scale(1.5);

            }

        }

        input[type="submit"] {
    background-color: #ff6b6b; /* Red color for the delete button */
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}

input[type="submit"]:hover {
    background-color: darken(#880907); /* Slightly darker red on hover */
}

        /* General search bar container styles, adjust as needed */
.search-container {
    margin: 20px;
    text-align: center; /* Center the search bar */
}


/* Styles for the search input */
.search-input {
    padding: 10px 15px;
    font-size: 16px; /* Larger font size for better readability */
    border: 1px solid #ddd; /* Light gray border */
    border-radius: 20px 0 0 20px; /* Rounded left corners */
    outline: none; /* Removes the outline */
    width: 60%; /* Set the width of the search input */
}

/* Styles for the search button */
.search-button {
    padding: 10px 15px;
    font-size: 16px; /* Matches the search input font size */
    border: 1px solid #7aa095; /* Border color to match the button */
    background-color: #7aa095; /* Bootstrap primary button color */
    color: white;
    border-radius: 0 20px 20px 0; /* Rounded right corners */
    cursor: pointer; /* Changes the cursor to a pointer */
    outline: none; /* Removes the outline */
    transition: background-color 0.3s ease; /* Smooth transition for hover effect */
}

/* Hover effect for button */
.search-button:hover {
    background-color: #567069; /* Darken button on hover */
    transform: scale(1.1);
}

/* Responsive adjustments for smaller screens */
@media (max-width: 768px) {
    .search-input,
    .search-button {
        border-radius: 20px; /* Fully rounded corners for mobile */
        margin-top: 10px; /* Add space between the elements */
        width: 100%; /* Full width for small screens */
    }
    .search-button {
        margin-top: 5px; /* Adjust space as needed */
    }
}
    </style>
</head>
<body>

    {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
        <div class="flash-{{ category }}" style="text-align: center;">{{ message }}</div>
        {% endfor %}
    {% endif %}
    {% endwith %}
    
    <div class="sidebar">
        <a href="{{ url_for('index') }}"><i class="fas fa-home"></i> Home</a>
        {% if session['logged_in'] %}
            <a href="{{ url_for('add_book') }}"><i class="fas fa-plus"></i> Add Book</a>
            <a href="{{ url_for('view_users') }}"><i class="fas fa-users"></i> Manage User</a>
            <a href="{{ url_for('logout') }}"><i class="fas fa-sign-out-alt"></i> Logout</a>
            
        {% else %}
            <a href="{{ url_for('login') }}"><i class="fas fa-sign-in-alt"></i> Login</a>
            <a href="{{ url_for('register') }}"><i class="fas fa-user-plus"></i> Register</a>
        {% endif %}
    </div>


    <div class="content">





        
        <div class="header">
            <h1>Library Management Dashboard</h1>
             {% if session['logged_in'] %}
        </div>
       
            <section>
                <h2>Available Books</h2>

            

                <div class="search-container">
                    <form method="post" action="/search">
                        <input type="text" name="search_query" class="search-filter" placeholder="Search...">
                        <select name="search_by">
                            <option value="title">Title</option>
                            <option value="author">Author</option>
                            <!-- Add more options for other fields -->
                        </select>
                        <button type="submit"  class="search-button">Search</button>
                    </form>

                </div>
                
                
                <div class="books-container">
                    {% for book in books %}
                        <div class="book-card">
                            <h3 class="book-title">{{ book.title }}</h3>
                            <p class="book-author">Author: {{ book.author }}</p>
                            <p class="book-author">Shelf: {{ book.shelf }}</p>
                            <div class="button-container">
                                <a class="btn update-btn" href="{{ url_for('update_book', book_id=book.id) }}">Update</a>
                                <form class="btn delete-btn" action="{{ url_for('delete_book', book_id=book.id) }}" method="POST" onclick="confirmDelete(123)">
                                    <input type="submit" value="Delete">
                                </form>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            </section>
        {% else %}
            <p>Please <a href="{{ url_for('login') }}">login</a> to see the book list.</p>
        {% endif %}
    </div>

    <script>
            function confirmDelete(bookId) {
            if (confirm('Are you sure you want to delete this book?')) {
                // User clicked 'OK', proceed with deletion
                $.ajax({
                    url: '/delete-book/' + bookId,  // Your API endpoint or route
                    type: 'DELETE',
                    success: function(result) {
                        // Handle success
                        alert('Book deleted successfully');
                        location.reload(); // Reloads the current page
                    },
                    error: function(err) {
                        // Handle errors
                        alert('Error deleting book');
                    }
                });
            } else {
                // User clicked 'Cancel', do nothing
                console.log('Deletion cancelled');
            }
        }


        let idleTime = 0;

            function resetIdleTime() {
                idleTime = 0;
            }

            function checkIdleTime() {
                idleTime++;
                if (idleTime >= 5) {  // 5 minutes
                    window.location.href = "{{ url_for('logout') }}";
                }
            }

            window.onload = function() {
                // Reset idle time on mouse movement, keypress, or touch
                document.onmousemove = resetIdleTime;
                document.onkeypress = resetIdleTime;
                document.ontouchstart = resetIdleTime;

                // Check idle time every minute
                setInterval(checkIdleTime, 60000); // 60000 milliseconds = 1 minute
            };
    </script>







</body>





</html>



