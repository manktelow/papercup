# Papercup

Given a json or srt file, generates an ASR representation in the following format:

```bash
[
    {
        text: string,
        startTime: number (seconds),
        endTime: number (seconds),
        duration: number (seconds)
    }
]
```

### To run

``` bash
poetry install
poetry shell

# run
python main.py assets/input.json
# or
python main.py assets/input.srt
```

### Tests
``` bash
poetry shell
python -m unittest discover services/tests
```