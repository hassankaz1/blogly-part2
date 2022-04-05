
from colorsys import TWO_THIRD
from unittest import TestCase
from app import app
from models import db, User, Post


class FlaskTests(TestCase):

    def setUp(self):
        """Set Up Function. Will run before any test"""
        self.client = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bogly'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True

        db.drop_all()
        db.create_all()

        one = User(first_name="Tom", last_name="Hanks",
                   image_url="https://media.npr.org/assets/img/2021/06/11/tom-hanks-29d69e8c39cd01d67c1a36d0a81674923d18577f.jpg")
        two = User(first_name="Chris", last_name="Hemsworth",
                   image_url="https://upload.wikimedia.org/wikipedia/commons/e/e8/Chris_Hemsworth_by_Gage_Skidmore_2_%28cropped%29.jpg")
        db.session.add(one)
        db.session.add(two)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_homepage(self):
        """Home Page, check status code to see if redirects to /users"""
        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)

    def test_user_list(self):
        with self.client:
            res = self.client.get('/users')
            html = res.get_data(as_text=True)
            self.assertIn('<a href="/users/1">Tom Hanks</a>', html)
            self.assertIn('<a href="/users/2">Chris Hemsworth</a>', html)

    def test_form_page(self):
        """test form page to add new user"""
        with self.client:
            res = self.client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(
                '<label for="fname" class="form-label">First Name</label>', html)
            self.assertIn(
                '<button type="submit" class="btn btn-primary">Save</button>', html)

    def test_form_input(self):
        """test if form creates new user by checking users list"""
        with self.client:
            res = self.client.post(
                '/users/new', data={"fname": "Hassan", "lname": "Kazi", "iurl": "https://cdn.vox-cdn.com/thumbor/o53k-QbKFns_s-OP89E8o34Ho8U=/0x0:599x500/1200x800/filters:focal(286x259:380x353)/cdn.vox-cdn.com/uploads/chorus_image/image/69634799/download__5_.0.jpg"}, follow_redirects=True)

            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<a href="/users/3">Hassan Kazi</a>', html)

    def test_user_profile(self):
        """Test Content of User Profile"""
        with self.client:
            res = self.client.get('/users/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h5 class="card-title">Tom Hanks</h5>', html)

    def test_post_form_input(self):
        """test if form creates new post for user"""
        with self.client:
            res = self.client.post(
                '/users/1/post-form', data={"title": "New Post", "content": "This is a new post"}, follow_redirects=True)

            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<a href="/posts/1">New Post</a>', html)
            self.assertIn('<p>Post &#39;New Post&#39; added.</p>', html)
