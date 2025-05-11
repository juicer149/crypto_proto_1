#!/usr/bin/env bash


# 1) Öppna alphabet.py i första tab
# 2) Ny tab: öppna base_cipher.py
# 3) Horisontell split i tab2: open base_substitutional_cipher.py under
# 4) Jämna ut alla splits

nvim \
  -c "e alphabet.py" \
  -c "tabnew base_cipher.py" \
  -c "split base_substitutional_cipher.py" \
  -c "wincmd ="

