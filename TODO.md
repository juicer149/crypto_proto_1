# TODO – Crypto Lab Architecture & Implementation

## ✅ Phase 1: Core Alphabet System
- [x] Create `Alphabet` class to handle:
  - [x] Loading from YAML (`from_config`)
  - [x] Caesar rotations via `__mul__` and `__rmul__`
  - [x] Substitution map generation
  - [x] Rotations generator (`rotations`)
  - [x] Implement `__str__` or `__repr__` for debugging clarity (optional)
  - [x] (Optional) Add `__contains__` and `as_list` property for safety and convenience

---

## 🔲 Phase 2: Config Handling
- [ ] Create `AppConfig` dataclass
  - [ ] Centralize config paths (e.g. `charsets.yaml`)
  - [ ] Possibly add defaults for common use cases (default language etc.)

---

## 🔲 Phase 3: Text Manipulation Utilities
- [ ] Create `text_manipulation.py` with `TextManipulator` class
  - [ ] `group_text()` — Group text into blocks (e.g., every 5 characters)
  - [ ] `pad_text()` — Pad text to block sizes with chosen character (e.g., `X`)
  - [ ] `filter_text()` — Clean text from invalid characters (optional)

---

## 🔲 Phase 4: Cipher Spec Handler (Advanced Symbol Handling)
- [ ] Create `CipherSpecHandler` module/class
  - [ ] Apply custom symbol rules, nomenclator, homophonic handling, etc.
  - [ ] Should be separate from `TextManipulator`
  - [ ] Can operate on text before encryption or on Alphabet level as optional pre-processing

---

## 🔲 Phase 5: Cipher Factory & Catalog System
- [ ] Create `CipherCatalog` with decorator-driven registration:
  - [ ] `@register_cipher(name)`
  - [ ] Central registry of cipher classes
- [ ] Implement `create_cipher(name, **kwargs)` dispatcher
- [ ] (Optional) Use `match/case` in CLI for argument parsing/dispatching

---

## 🔲 Phase 6: CLI / Interactive Interface
- [ ] Build CLI or REPL-style app:
  - [ ] Allow user to select cipher
  - [ ] Input text, key, and customization (group size, padding, etc.)
  - [ ] Dynamically show available ciphers from `CipherCatalog`
  - [ ] Use `TextManipulator` and `CipherSpecHandler` in the pipeline

---

## 🛠 Phase 7: Future / Advanced Ideas
- [ ] Implement heuristics for cipher identification (e.g., using `match/case`)
- [ ] Implement auto-analysis tools (frequency analysis, index of coincidence, etc.)
- [ ] Build visualization tools (output rotations, substitution maps, etc.)
- [ ] Add plugin system for user-contributed ciphers and specs

---


---

### Notes:
- Keep cipher logic, text manipulation, and config separate for clean responsibilities.
- Alphabet should remain as the **pure data layer**.
- Cipher behavior, manipulation, and UI should operate in higher abstraction layers.
- Follow Pythonic patterns (decorators, factory, class methods, duck typing).


