# DESIGN.md – Crypto Lab Project

## Purpose
This project aims to create a clean, modular, and extensible framework for working with classical ciphers (mono- and polyalphabetic), text manipulations, and cipher-specific rules (like nomenclators, homophones, etc.).

The goal is to separate responsibilities clearly, keep the system testable and composable, and allow for both user-driven CLI operations and automated cipher analysis.

---

## Core Principles

### 1. Clean separation of concerns
- **Alphabet**: Pure data object representing a cipher alphabet.
- **TextManipulator**: Pure utilities for transforming plaintext/ciphertext (grouping, padding, etc.).
- **CipherSpecHandler**: Applies cipher-specific manipulations (e.g., special substitutions, nomenclator rules).
- **CipherCatalog & Factory**: Abstracts cipher class creation and allows easy extension using decorators.
- **CLI / App Layer**: Handles user interaction, cipher selection, and orchestration of manipulation and ciphering.

### 2. Composability
Each layer can be used independently or combined flexibly:
- `Alphabet` can be used in manual ciphers or pipelines.
- `TextManipulator` can be reused in any cipher context.
- `CipherSpecHandler` can wrap any text before ciphering.

### 3. Config-driven architecture
- All resources, such as charsets and possible cipher specs, should be loaded via a centralized `AppConfig` class or module.
- This allows users to expand or override the system without modifying the codebase.

---

## Architecture Overview

+---------------------------+
| Config (AppConfig) |
+---------------------------+
↓
+---------------------------+
| Alphabet |
| - Load from YAML |
| - Caesar rotation |
| - Substitution map |
| - Rotation generator |
+---------------------------+
↓
+---------------------------+
| CipherSpecHandler |
| - Nomenklators |
| - Homophonic handling |
+---------------------------+
↓
+---------------------------+
| TextManipulator |
| - Grouping |
| - Padding |
| - Filtering (optional) |
+---------------------------+
↓
+---------------------------+
| CipherCatalog / Factory |
| - Decorator registry |
| - Dispatcher |
+---------------------------+
↓
+---------------------------+
| CLI / App Interface |
+---------------------------+



---

## Key Design Choices

- **Alphabet as a pure, immutable data model.**
- **All manipulation is done outside of the cipher logic itself**, ensuring cipher classes are minimal and focused only on encryption/decryption logic.
- **Cipher-specific rules (nomenklators, custom mappings)** are handled separately in `CipherSpecHandler`.
- **Use of `match/case` (Python 3.10+) where clear branching on types or cipher names improves readability.**
- **Factory pattern combined with decorator registration ensures easy expansion of new ciphers without touching the catalog logic.**

---

## Future Expandability
- Add support for cipher detection and attack strategies (`Analyzer` module).
- Allow runtime expansion of alphabets, specs, and ciphers via plugin system.
- Provide visual tools for substitution maps, rotations, and frequency analysis.
- Extend CLI to support pipelines (e.g., `plaintext → spec handler → cipher → manipulator → output`).

---

## Design Philosophy Summary

| Layer                  | Responsibility                         | Type              |
|------------------------|----------------------------------------|-------------------|
| Config (`AppConfig`)    | Central config values, paths           | Static config     |
| Alphabet                | Data model for alphabets               | Data layer        |
| CipherSpecHandler       | Cipher-specific symbol manipulation    | Domain logic      |
| TextManipulator         | General text manipulation              | Utility layer     |
| CipherCatalog/Factory   | Dynamic cipher registration/dispatch   | Abstract factory  |
| CLI / App Interface     | User-facing app or CLI orchestration   | UI / Integration  |

---

## Notes

- Each component is small, single-purpose, and testable.
- Avoids unnecessary inheritance; favors composition and decorators.
- Keeps ciphers as dumb objects that rely on injected alphabet, spec handler, and manipulator pipelines.


