# core/pipeline_factory.py

from engines.registry import ENGINE_REGISTRY
import jsonschema
from config_loader import load_config


def validate_pipeline_config(config_data, schema_file):
    """
    Loads config (YAML or JSON), validate, builds pipelines with registry.
    """
    schema = load_config(schema_file)
    jsonschema.validate(instance=config_data, schema=schema)


def create_pipelines_from_config(config_file, alphabet, schema_file):
    """
    Laddar config (YAML eller JSON), validerar, bygger pipelines via registry.
    """
    config = load_config(config_file)
    validate_pipeline_config(config, schema_file)
    
    pipelines = {}
    for cipher_name, steps in config["pipelines"].items():
        engines = [
            ENGINE_REGISTRY[step["engine"]](step, alphabet) for step in steps
        ]
        pipelines[cipher_name] = engines
    return pipelines
