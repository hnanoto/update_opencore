"""Testes para o módulo logger."""
import unittest
import tempfile
import os
import json
from unittest.mock import patch, mock_open
import sys
import os

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logger import get_system_language, get_translation, log


class TestLogger(unittest.TestCase):
    """Testes para as funções do módulo logger."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.temp_dir = tempfile.mkdtemp()
        self.translations_dir = os.path.join(self.temp_dir, "translations")
        os.makedirs(self.translations_dir)

    def tearDown(self):
        """Limpeza após os testes."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_get_system_language_basic(self):
        """Testa a detecção básica do idioma do sistema."""
        with patch('locale.getlocale') as mock_getlocale:
            mock_getlocale.return_value = ('pt_BR', 'UTF-8')
            result = get_system_language()
            self.assertEqual(result, 'pt_BR')

    def test_get_system_language_fallback(self):
        """Testa o fallback para inglês quando não consegue detectar o idioma."""
        with patch('locale.getlocale') as mock_getlocale:
            mock_getlocale.return_value = (None, None)
            with patch.dict(os.environ, {}, clear=True):
                result = get_system_language()
                self.assertEqual(result, 'en')

    def test_get_translation_with_fallback(self):
        """Testa a obtenção de tradução com fallback."""
        # Simula traduções carregadas
        test_translations = {
            'en': {'test_key': 'Test Value'},
            'pt': {'test_key': 'Valor de Teste'}
        }
        
        with patch('logger.TRANSLATIONS', test_translations):
            # Testa tradução em português
            with patch('logger.get_system_language', return_value='pt'):
                result = get_translation('test_key')
                self.assertEqual(result, 'Valor de Teste')
            
            # Testa fallback para inglês
            with patch('logger.get_system_language', return_value='fr'):
                result = get_translation('test_key')
                self.assertEqual(result, 'Test Value')
            
            # Testa retorno da chave quando não encontra tradução
            with patch('logger.get_system_language', return_value='fr'):
                result = get_translation('nonexistent_key')
                self.assertEqual(result, 'nonexistent_key')

    def test_get_translation_no_fallback(self):
        """Testa a obtenção de tradução sem fallback."""
        test_translations = {
            'en': {'test_key': 'Test Value'}
        }
        
        with patch('logger.TRANSLATIONS', test_translations):
            with patch('logger.get_system_language', return_value='fr'):
                result = get_translation('test_key', fallback_to_key=False)
                self.assertIsNone(result)

    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_log_function(self, mock_print, mock_file):
        """Testa a função de log."""
        test_message = "Test log message"
        log(test_message)
        
        # Verifica se a mensagem foi impressa
        mock_print.assert_called_once_with(test_message)
        
        # Verifica se a mensagem foi escrita no arquivo
        mock_file.assert_called()
        mock_file().write.assert_called_with(test_message + "\n")


if __name__ == '__main__':
    unittest.main()
