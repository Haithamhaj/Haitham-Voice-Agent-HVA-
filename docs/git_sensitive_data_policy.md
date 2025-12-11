# Git Sensitive Data Policy

**Last Updated:** 2025-12-11

## Overview
This repository contains configuration and code for the Haitham Voice Agent. It is critical that **personal data, raw datasets, and media files** are NEVER committed to Git.

## Protected Paths
The following paths are explicitly ignored in `.gitignore` and must remain untracked:

### Private Data & Datasets
- `Haitham Data/` (Raw Source Material)
- `haithm_corpus/` (Ingestion Staging Area)
- `data/haithm_corpus_raw*.jsonl` (Normalized Raw Corpus)
- `data/dataset_haithm_*.jsonl` (Finetuning Datasets)
- `data/dataset_hva_qwen_routing.jsonl`

### Media Files
- Audio: `*.m4a`, `*.mp3`, `*.wav`, `*.aac`, `*.ogg`, `*.flac`
- Images: `*.png`, `*.jpg`, `*.jpeg`, `*.webp`

## Incident Report: `data/haithm_corpus_raw.jsonl`
- **Detection**: This file was found in the Git index (tracked).
- **Action**: It has been removed from the index using `git rm --cached` (file remains on disk).
- **History Check**: The file was present in commit `d5699a6`.
- **Verdict**: Inspection confirmed it contained **only dummy test data** (3 records). **No history rewrite is required.**

## How to Add New Private Data
1. Place files in `Haitham Data/` or `haithm_corpus/`.
2. Ensure `.gitignore` covers the file extension or directory.
3. Run `git status` to confirm the file is ignored.

## Enforcement
- Always run `git status` before committing.
- If a sensitive file appears in "Untracked files", update `.gitignore` immediately.
