# Juliet
Linguo is a chatbot implemented with Rasa framework, to get the daily news in Basque. This project has been developed with the [IXA research group](http://ixa.si.ehu.es/) as a bachelor's degree final thesis, and directed by [Gorka Azkune](https://gazkune.github.io/) and [Eneko Agirre](https://eagirre.github.io/).

## Installation

Juliet can be installed from GitHub:

```bash
git clone https://github.com/igabirondo16/Juliet.git
```
Install neccesary dependencies for this project:
```bash
python3 -m pip install -r requirements.txt
```


## Usage

First of all, retraining Rasa's model is recommended:
```bash
rasa train
```

After that, ngrok tunnel must be deployed. This step can also be done with [NgrokTunnelGenerator](https://github.com/igabirondo16/NgrokTunnelGenerator).

```bash
ngrok http 5005
```

Update Juliet's database with daily news:
```python
python3 ./utils/scheduler.py
```

Start Rasa action server:

```bash
rasa run actions
```

Finally, start Rasa server:

```bash
rasa run
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
Apache License 2.0
