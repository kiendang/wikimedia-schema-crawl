scripts to download MediaWiki EventLogging schemas https://www.mediawiki.org/wiki/Extension:EventLogging

requires python >= 3.8

```sh
cp config.example.yaml config.yaml
python get_schema_list_async.py
python download.py
```
