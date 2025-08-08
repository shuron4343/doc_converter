"""
CLI интерфейс для конвертера документов
"""

import click
import logging
from pathlib import Path
from .converter import DocumentConverter


def setup_logging(verbose: bool):
    """Настройка логирования"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Подробный вывод')
@click.pass_context
def cli(ctx, verbose):
    """Конвертер документов в markdown с помощью docling"""
    setup_logging(verbose)
    ctx.ensure_object(dict)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--config', '-c', type=click.Path(), help='Файл конфигурации')
def convert(input_file, output_file, config):
    """Конвертирует документ в markdown"""
    converter = DocumentConverter()
    
    # Проверяем поддерживается ли формат
    if not converter.is_supported_format(input_file):
        supported = ', '.join(converter.get_supported_formats())
        click.echo(f"Неподдерживаемый формат файла. Поддерживаемые форматы: {supported}")
        return 1
    
    # Конвертируем документ
    success = converter.convert(input_file, output_file)
    
    if success:
        click.echo(f"✅ Конвертация завершена: {output_file}")
        return 0
    else:
        click.echo("❌ Ошибка при конвертации")
        return 1


@cli.command()
def formats():
    """Показывает поддерживаемые форматы"""
    converter = DocumentConverter()
    supported = converter.get_supported_formats()
    click.echo("Поддерживаемые форматы:")
    for fmt in supported:
        click.echo(f"  - {fmt}")


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def info(input_file):
    """Показывает информацию о файле"""
    file_path = Path(input_file)
    converter = DocumentConverter()
    
    click.echo(f"Файл: {file_path.name}")
    click.echo(f"Размер: {file_path.stat().st_size} байт")
    click.echo(f"Формат: {file_path.suffix}")
    click.echo(f"Поддерживается: {'✅' if converter.is_supported_format(input_file) else '❌'}")


def main():
    """Точка входа для CLI"""
    cli()


if __name__ == '__main__':
    main()
