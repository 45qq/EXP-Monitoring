import os
import yaml

root_dir = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
config_file = os.path.join(root_dir, 'config.yaml')

with open(config_file, 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    github_monitor_config = config['github_monitor_config']
    schedule = config['schedule']

if __name__ == '__main__':
    print(config)
