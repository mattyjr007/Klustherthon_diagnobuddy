import sys
import os
# getting the name of the directory
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
 
import unittest
from models import SessionManager, Model

class TestModel(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_chatBot(self):
        model = Model()
        session_manager = SessionManager()
        session_id = "test_session"

        # Test the chatBot method
        message = "I have headaches"
        response, chat_history = model.chatBot(message, session_manager.get_session(session_id))
        self.assertIsInstance(response, str)
        self.assertIsInstance(chat_history, list)

    def test_chatBotLang(self):
        model = Model()

        # Test the chatBotLang method
        message = "I have headaches"
        response = model.chatBotLang(message)
        self.assertIsInstance(response, str)

    def test_chatLlama2(self):
        model = Model()

        # Test the chatLlama2 method
        message = "I have headaches"
        response = model.chatLlama2(message)
        self.assertIsInstance(response, str)

    def test_session_manager(self):
        session_manager = SessionManager()
        session_id = "test_session"

        # Test the session manager methods
        session = session_manager.get_session(session_id)
        self.assertIsInstance(session, dict)

        session_manager.update_last_activity(session_id)
        self.assertIsNotNone(session_manager.sessions[session_id]["last_activity"])

        chat_history = [{"role": "user", "content": "Describe symptoms"}]
        session_manager.updatesessionchat(session_id, chat_history)
        self.assertEqual(session_manager.sessions[session_id]["chatshistory"], chat_history)

        # Ensure clearing expired sessions doesn't raise an exception
        session_manager.clear_expired_sessions()

if __name__ == '__main__':
    unittest.main()
