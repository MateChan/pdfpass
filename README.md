# pdfpass

A simple CLI tool to add password protection to PDF files.

Mostly for my own use.

...in some lab somewhere, this would be extremely useful, shouldn't it?

## Prerequisites

- [uv](https://docs.astral.sh/uv/) - Python package and project manager

## Installation

```bash
uv tool install git+https://github.com/MateChan/pdfpass.git
```

## Usage

```bash
pdfpass path/to/your/file.pdf
```

The tool will prompt for user and owner passwords. The encrypted PDF will be saved as `file-pass.pdf`.

## Options

- `-u` - User password (optional, will prompt if not provided)
- `-o` - Owner password (optional, will prompt if not provided)

## Example

```bash
pdfpass document.pdf -u userpass -o ownerpass
```
