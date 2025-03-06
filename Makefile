run:
    python main.py --from $(sender) --to $(recipient) --text "$(message)"

test:
    pytest tests/

lint:
    poetry run flake8 .

format:
    poetry run black .

clean:
    rm -rf logs/*.log