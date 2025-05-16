# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## \[Unreleased]

### Added

* Introduced a modular and layered project structure with directories:

  * `core`: Manages pipeline creation, execution, and validation.
  * `engines`: Contains specific cipher engines implementations.
  * `tools`: Provides reusable utilities for alphabets, text manipulation, and message handling.
  * `config`: Centralizes configuration files.
* Added `config_loader.py` capable of handling both YAML and JSON configuration files.
* Created generic and reusable `SequenceManipulator` class (`lib/sequencemanipulator.py`) for domain-neutral sequence operations, including strict validation and rotation capabilities.
* Implemented mixins for composable sequence transformations:

  * `KeywordMixin` for keyword-based sequence manipulations.
  * `RotMixin` for ROT-style sequence rotations.
* Refined `Alphabet` class (`lib/dataclasses/alphabet.py`) to leverage `SequenceManipulator`, supporting dynamic rotations, keyword manipulations, and substitutions.
* Enhanced safe string handling with `MessageBit` (`tools/message_bit.py`) providing clean methods for text grouping, padding, and whitespace management.
* Refactored `TextManipulator` (`tools/text_manipulator.py`) to consistently return `MessageBit` objects.
* Created `engines/rot.py` featuring a unified ROT engine abstraction (`AbstractRotEngine`) and concrete implementations:

  * Static ROT (Caesar, ROT13)
  * Alberti ROT (progressive shifts)
  * Vigenère ROT (keyword-based shifts)
* Created `engines/plugboard.py` supporting static plugboard mappings.
* Implemented dynamic engine registration via `engines/registry.py`.
* Built `core/pipeline_factory.py` and `core/pipeline_runner.py` for YAML/JSON-driven cipher pipelines with schema validation (`core/schema.json`).
* Established a clear architecture and API layering model documented in `docs/arcitecur_layer.md`.

### Changed

* Refactored monolithic cipher classes into decoupled engines and modular pipelines.
* Migrated from a hardcoded cipher catalog to a flexible registry and factory design pattern.
* Standardized all cipher configurations via external files (`charsets.yaml`, `cipher.yaml`) enhancing configurability and CLI usability.
* Replaced old hardcoded cipher logic (Caesar, ROT, Alberti) with composable ROT engines.
* Updated text handling to exclusively use `MessageBit` for safer string operations and clearer codebase.

### Removed

* Deprecated legacy files:

  * `alphabet.py`
  * `base_cipher.py`
  * `base_substitutional_cipher.py`
  * `cipher_catalog.py`
  * `cipher_factory.py`
  * `load_yaml.py`
  * `rot_engine.py`
  * Old `message_bit.py` and `text_manipulator.py` (replaced by versions in `tools`)

### Deprecated

* N/A

---

## \[0.1.0] - Initial Experimentation Phase

### Added

* Initial prototypes for basic ciphers (Caesar, ROT), message handling, and substitution mapping.
* Basic configuration handling and alphabet utilities.
* Simple CLI scripts for experimental cipher implementations.

### Notes

* This version marked the exploratory phase before modular refactoring and structured layering were introduced.

