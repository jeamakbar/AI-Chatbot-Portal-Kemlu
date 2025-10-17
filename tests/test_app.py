import unittest
import json
from unittest.mock import patch, Mock
import os

# Set dummy environment variables before importing the app
os.environ['LLM_API_KEY'] = 'test-key'
os.environ['LLM_MODEL'] = 'test-model'

import app
from constants import GENERIC_FALLBACK

class TestApp(unittest.TestCase):

    def setUp(self):
        """
        Set up a test client for the Flask application and initialize the link map.
        """
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        app.build_link_map()
        # Clear all caches and histories for each test to ensure isolation
        app.llm_cache.clear()
        app.conversation_histories.clear()
        app.session_contexts.clear()
        app.session_triggered_keywords.clear()

    # --- Test Helper Functions ---

    def test_replace_link_placeholders(self):
        """
        Tests the replacement of [LINK:...] placeholders with HTML <a> tags.
        """
        # Test a valid placeholder
        text = "For more info, see [LINK:Layanan Konsuler]."
        expected = 'For more info, see <a href="https://kemlu.go.id/layanan/layanan-konsuler-fasilitas-diplomatik-dan-pelindungan-wni/kekonsuleran" target="_blank">Layanan Konsuler</a>.'
        self.assertEqual(app.replace_link_placeholders(text), expected)

        # Test an invalid placeholder
        text_invalid = "This is a [LINK:nonexistent link]."
        expected_invalid = "This is a nonexistent link."
        self.assertEqual(app.replace_link_placeholders(text_invalid), expected_invalid)

    def test_format_perwakilan_list_items(self):
        """
        Tests the HTML formatting for representative office details.
        """
        test_info = {
            "name": "KBRI Tokyo",
            "address": "5-2-9 Higashigotanda, Shinagawa",
            "telepon": "+81-03-3441-4201",
            "link": "https://kemlu.go.id/tokyo"
        }
        # Test in Indonesian
        html_id = app.format_perwakilan_list_items(test_info, 'id')
        self.assertIn("<b>Alamat:</b> 5-2-9 Higashigotanda, Shinagawa", html_id)
        self.assertIn("<b>Situs Web:</b> <a href='https://kemlu.go.id/tokyo'", html_id)

        # Test in English
        html_en = app.format_perwakilan_list_items(test_info, 'en')
        self.assertIn("<b>Address:</b> 5-2-9 Higashigotanda, Shinagawa", html_en)
        self.assertIn("<b>Website:</b> <a href='https://kemlu.go.id/tokyo'", html_en)

    # --- Test Core Logic ---

    @patch('app.find_location_info')
    def test_handle_address_request(self, mock_find_location):
        """
        Tests the address request handler logic.
        """
        mock_location_data = {
            "name": "KBRI Tokyo", "address": "Tokyo Address", "link": "http://tokyo.com",
            "wilayah_akreditasi": "Jepang", "telepon": "123", "fax": "456", "email": "a@b.com"
        }
        mock_find_location.return_value = (mock_location_data, 95)

        query = "di mana alamat kbri tokyo?"
        result = app.handle_address_request(query, 'id')
        self.assertIsNotNone(result)
        reply, _, response_type, _ = result

        self.assertEqual(response_type, "address_request")
        self.assertIn("Informasi untuk KBRI Tokyo", reply)
        self.assertIn("Tokyo Address", reply)
        
    @patch('app.find_location_info')
    def test_handle_lost_document(self, mock_find_location):
        """
        Tests the lost document handler for both found and not-found scenarios.
        """
        # Scenario 1: Location found
        mock_location_data = {"name": "KBRI Berlin", "address": "Alamat Berlin"}
        mock_find_location.return_value = (mock_location_data, 95)
        
        reply, _, response_type, _ = app.handle_lost_document("paspor saya hilang di berlin", 'id')
        self.assertEqual(response_type, "lost_document")
        self.assertIn("Panduan Kehilangan Dokumen di KBRI Berlin", reply)
        self.assertIn("Alamat Berlin", reply)

        # Scenario 2: Location NOT found
        mock_find_location.return_value = (None, 0)
        reply, _, response_type, _ = app.handle_lost_document("dokumen hilang di kota antah berantah", 'id')
        self.assertEqual(response_type, "lost_document_generic")
        self.assertIn("Mohon informasikan di kota dan negara mana Anda berada", reply)

    # --- Test Flask Routes ---
    
    @patch('app.db', None)
    @patch('app.requests.post')
    @patch('app.retrieve_relevant_info')
    def test_ask_endpoint(self, mock_retrieve, mock_post):
        """
        Comprehensive test for the /ask endpoint, covering various scenarios.
        """
        session_id = "test-session-123"

        # 1. Test Greeting
        response = self.client.post('/ask', json={'message': 'halo', 'language': 'id', 'session_id': session_id})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['reply'], "Halo! Ada yang bisa saya bantu?")

        # 2. Test Keyword Match (Passport)
        response = self.client.post('/ask', json={'message': 'cara buat paspor', 'language': 'id', 'session_id': session_id})
        data = response.get_json()
        self.assertIn("Pengajuan atau Perpanjangan Paspor Indonesia", data['reply'])
        self.assertIn("Berapa biaya pembuatan paspor?", data['follow_up'])
        
        self.assertEqual(app.session_contexts[session_id], ['layanan konsuler'])

        app.session_contexts.clear()

        # 3. Test LLM Fallback (Successful)
        # Ensure RAG finds nothing to test the generic fallback
        mock_retrieve.return_value = None

        mock_llm_response = Mock()
        mock_llm_response.status_code = 200
        mock_llm_response.json.return_value = {
            "choices": [{"message": {"content": "Ini adalah jawaban dari AI.###Follow up 1?|Follow up 2?"}}]
        }
        mock_post.return_value = mock_llm_response
        
        response = self.client.post('/ask', json={'message': 'pertanyaan tidak ada di keyword', 'language': 'id', 'session_id': session_id})
        data = response.get_json()
        self.assertEqual(data['reply'], "Ini adalah jawaban dari AI.")
        self.assertEqual(data['follow_up'], ["Follow up 1?", "Follow up 2?"])
        mock_post.assert_called_once()

        # 4. Test LLM Fallback (API Failure) -> Static Fallback
        mock_post.reset_mock()
        mock_post.side_effect = app.requests.exceptions.RequestException("API Error")

        response = self.client.post('/ask', json={'message': 'saya mau tanya alamat kbri', 'language': 'id', 'session_id': session_id})
        data = response.get_json()
        self.assertIn("Informasi Perwakilan RI", data['reply'])
        self.assertIn("halaman Perwakilan di situs resmi Kemlu", data['reply'])

        # 5. Test LLM Fallback (API Failure) -> Generic Fallback
        response = self.client.post('/ask', json={'message': 'random question with no fallback', 'language': 'id', 'session_id': session_id})
        data = response.get_json()
        self.assertEqual(data['reply'], GENERIC_FALLBACK['id'])

    def test_missing_session_id(self):
        """
        Tests that the API returns an error if session_id is missing.
        """
        response = self.client.post('/ask', json={'message': 'hello', 'language': 'en'})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("session_id is missing", data['reply'])

    @patch('app.db')
    def test_report_endpoint(self, mock_db):
        """
        Tests the /report endpoint and Firestore interaction.
        """
        mock_collection = mock_db.collection.return_value
        mock_doc = mock_collection.document.return_value

        response = self.client.post('/report', json={
            'session_id': 'test-session',
            'feedback': 'AI nya sangat membantu!'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')
        
        mock_db.collection.assert_called_with('feedback')
        mock_collection.document.assert_called_once()
        mock_doc.set.assert_called_once()

    @patch('app.db')
    def test_feedback_endpoint(self, mock_db):
        """
        Tests the /feedback (review) endpoint and Firestore interaction.
        """
        mock_collection = mock_db.collection.return_value
        mock_doc = mock_collection.document.return_value

        response = self.client.post('/feedback', json={
            'session_id': 'test-session',
            'vote': 'up',
            'message': 'Jawaban bagus'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')

        mock_db.collection.assert_called_with('review')
        mock_collection.document.assert_called_once()
        mock_doc.set.assert_called_once()


if __name__ == '__main__':
    unittest.main()