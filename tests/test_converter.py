"""
Тесты для DocumentConverter
"""

import pytest
import tempfile
import os
from pathlib import Path
from doc_converter.converter import DocumentConverter


class TestDocumentConverter:
    """Тесты для класса DocumentConverter"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.converter = DocumentConverter()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Очистка после каждого теста"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_supported_formats(self):
        """Тест получения поддерживаемых форматов"""
        formats = self.converter.get_supported_formats()
        assert isinstance(formats, list)
        assert '.docx' in formats
        assert '.pdf' in formats
    
    def test_is_supported_format(self):
        """Тест проверки поддерживаемого формата"""
        assert self.converter.is_supported_format('test.docx')
        assert self.converter.is_supported_format('test.PDF')
        assert not self.converter.is_supported_format('test.xyz')
    
    def test_convert_nonexistent_file(self):
        """Тест конвертации несуществующего файла"""
        output_path = os.path.join(self.temp_dir, 'output.md')
        result = self.converter.convert('nonexistent.docx', output_path)
        assert result is False
    
    def test_convert_creates_output_dir(self):
        """Тест создания выходной директории"""
        # Создаем временный входной файл
        input_file = os.path.join(self.temp_dir, 'test.txt')
        with open(input_file, 'w') as f:
            f.write('Test content')
        
        # Пытаемся конвертировать в несуществующую директорию
        output_path = os.path.join(self.temp_dir, 'subdir', 'output.md')
        result = self.converter.convert(input_file, output_path)
        
        # Проверяем что директория была создана
        assert os.path.exists(os.path.dirname(output_path))
    
    def test_convert_success(self):
        """Тест успешной конвертации"""
        # Создаем временный входной файл
        input_file = os.path.join(self.temp_dir, 'test.txt')
        with open(input_file, 'w') as f:
            f.write('Test content')
        
        output_path = os.path.join(self.temp_dir, 'output.md')
        result = self.converter.convert(input_file, output_path)
        
        assert result is True
        assert os.path.exists(output_path)
        
        # Проверяем содержимое выходного файла
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Конвертированный документ' in content
            assert 'test.txt' in content


class TestDocumentConverterConfig:
    """Тесты для конфигурации DocumentConverter"""
    
    def test_init_with_config(self):
        """Тест инициализации с конфигурацией"""
        config = {'test': 'value'}
        converter = DocumentConverter(config)
        assert converter.config == config
    
    def test_init_without_config(self):
        """Тест инициализации без конфигурации"""
        converter = DocumentConverter()
        assert converter.config == {}


if __name__ == '__main__':
    pytest.main([__file__])
