from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<table', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            data = response.get_json()

            # test version a
            self.assertIsInstance(data['gameId'], str)
            # test that the board is a list
            self.assertIsInstance(data['board'], list)
            # test that the game_id is in the dictionary of games (imported from app.py above)
            self.assertIn(data['gameId'], games)

    def test_score_word(self):
        """Test if word is valid"""

        with self.client as client:
            # make a post request to /api/new-game
            new_game_response = client.post('/api/new-game')

            # get the response body as json using .get_json()
            data = new_game_response.get_json()

            # find that game in the dictionary of games (imported from app.py above)
            game = games[data['gameId']]

            # manually change the game board's rows so they are not random
            game.board = [['A', 'B', 'T', 'G', 'V'],
                            ['R', 'D', 'E', 'Y', 'N'],
                            ['E', 'B', 'E', 'E', 'E'],
                            ['E', 'E', 'U', 'I', 'R'],
                            ['S', 'E', 'S', 'A', 'M']]

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            valid_word_response = client.post('/api/score-word',
                                              json = {
                                                  "gameId": data['gameId'],
                                                  "word": "SEE"
                                              })
            valid_word_data = valid_word_response.get_json()

            self.assertEqual(valid_word_data, {'result': 'ok'})

            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            not_on_board_response = client.post('/api/score-word',
                                              json = {
                                                  "gameId": data['gameId'],
                                                  "word": "ZUZ"
                                              })
            not_on_board_data = not_on_board_response.get_json()

            self.assertEqual(not_on_board_data, { 'result': 'not-on-board'})

            # test to see that an invalid word returns {'result': 'not-word'}
            not_a_word_response = client.post('/api/score-word',
                                              json = {
                                                  "gameId": data['gameId'],
                                                  "word": "AWRHTAETGAWRETH"
                                              })
            not_a_word_data = not_a_word_response.get_json()

            self.assertEqual(not_a_word_data, { 'result': 'not-word'})