# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- Introduced modular project structure with `core`, `engines`, `tools`, and `config` directories.
- Created `config_loader.py` to handle both YAML and JSON loading, replacing old hardcoded loaders.
- Added `tools/alphabet.py` as a composable, reusable Alphabet class supporting rotations and substitutions.
- Added `tools/message_bit.py` for safe string handling, grouping, and padding, with clean API.
- Added `tools/text_manipulator.py` refactored to return `MessageBit` for all operations.
- Created `engines/rot.py` with unified ROT engine abstraction (`AbstractRotEngine`) and implementations for:
  - Static ROT (e.g., Caesar, ROT13)
  - Alberti ROT (progressive shift)
  - Vigenère ROT (keyword-based shift)
- Created `engines/plugboard.py` for static plugboard mapping support.
- Created `engines/registry.py` with dynamic engine registration system.
- Created `core/pipeline_factory.py` and `core/pipeline_runner.py` supporting YAML-driven pipelines of engines.
- Created `core/schema.json` for strict JSON Schema validation of cipher pipelines.
- Implemented dynamic pipeline composition and substitution chaining using `CipherPipeline`.

### Changed
- Refactored old monolithic cipher classes into decoupled engines and pipelines.
- Removed hardcoded cipher catalog and replaced with registry + factory pattern.
- Improved configurability and CLI-friendliness by relying entirely on config files for pipelines, alphabets, and engines.
- Replaced all hardcoded ROT, Caesar, Alberti logic with composable ROT engines.
- Cleaned up text handling by introducing `MessageBit` instead of handling raw strings directly.

### Removed
- Deleted legacy files:
  - `alphabet.py`
  - `base_cipher.py`
  - `base_substitutional_cipher.py`
  - `cipher_catalog.py`
  - `cipher_factory.py`
  - `load_yaml.py`
  - `rot_engine.py`
  - `message_bit.py` (replaced by `tools/message_bit.py`)
  - `text_manipulator.py` (replaced by `tools/text_manipulator.py`)

### Deprecated
- N/A

---

## [0.1.0] - Initial Experimentation Phase

### Added
- First prototypes for Caesar cipher, ROT engine, message handling, and substitution mapping.
- Created basic config handling and alphabet utilities.
- Wrote minimal CLI for testing cipher implementations.
- Added first experimental Python scripts in flat structure.

### Notes
- This phase was exploratory, before introducing the layered and modular refactoring done later.

