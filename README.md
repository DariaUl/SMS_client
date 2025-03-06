# SMS Client CLI

## Описание

Программа-клиент для отправки SMS-сообщений через условный сервис. Реализована на Python с использованием только стандартной библиотеки socket без сторонних HTTP-библиотек.

Основные функции:
- Отправка SMS через командную строку.
- Конфигурация через TOML-файл.
- Логирование действий с маскировкой чувствительных данных (например, номеров телефонов).
- Поддержка повторных попыток при сетевых ошибках.


## Требования

- Python 3.8+
- Poetry для управления зависимостями.
- Makefile для удобного запуска.
- Мок-сервер Prism для тестирования API (опционально).


## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/your-repo/sms_client.git
   cd sms_client

2. **Установите зависимости через Poetry:**
   ```
   poetry install

3. **Создайте файл конфигурации config.toml:**
   ```
   base_url = "http://localhost:4010"
   username = "user"
   password = "pass"

4. **Установите и запустите мок-сервер:**  
   1. Скачать Prism для своей платформы:  
   Windows / Linux / macOS: https://github.com/stoplightio/prism/releases 
   2. Запустить мок-сервер: 
   ```
   Linux: ./prism-cli-linux mock sms-platform.yaml 
   macOS: ./prism-cli-macos mock sms-platform.yaml 
   Windows: ./prism-cli-win.exe mock sms-platform.yaml 