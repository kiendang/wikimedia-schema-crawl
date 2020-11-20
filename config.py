from ruamel.yaml import YAML


yaml = YAML(typ='safe')

with open('config.yaml', 'r') as f:
    config = yaml.load(f)
