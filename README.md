# Extract Code Blocks from Markdown GitHub Action

This action extracts code blocks of a specified programming language from markdown files and saves them to one or more output files.

## Inputs

### `input_file`

**Required** The path to the input markdown file.

### `output_file`

**Optional** The path to the output file. If not specified, the output will be saved to a file named `extracted_<input_filename>_<language>.<extension>` in the same directory as the input file.

### `language`

**Optional** The programming language of code blocks to extract. Default is `javascript`.

### `block_number`

**Optional** The specific block number to extract (1-indexed). If not specified, all blocks of the specified language will be extracted to separate files.

## Example usage

### Extract all JavaScript code blocks

```yaml
- uses: your-username/action-extract-doc-code@v1
  with:
    input_file: docs/example.md
```

### Extract a specific Python code block

```yaml
- uses: your-username/action-extract-doc-code@v1
  with:
    input_file: docs/example.md
    output_file: src/example.py
    language: python
    block_number: 2
```

## Example workflow

```yaml
name: Validate Documentation Code Examples
on:
  push:
    paths:
      - 'docs/**/*.md'

jobs:
  lint-code-examples:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Extract JavaScript examples
        uses: your-username/action-extract-doc-code@v1
        with:
          input_file: docs/api-guide.md
          language: javascript
          output_file: temp/extracted-code.js
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '16'
          
      - name: Install ESLint
        run: npm install eslint
        
      - name: Lint extracted code
        run: npx eslint temp/extracted-code*.js
        
      - name: Report results
        if: success()
        run: echo "✅ All code examples in documentation pass linting!"
```

## Features

- Extract code blocks of a specific language from markdown files
- Save all blocks to separate files or extract a specific block
- Automatically determine output file extension based on language
- Create output directories if they don't exist

## Supported Languages

The action supports various programming languages, including:

- JavaScript (outputs as TypeScript .ts files by default)
- Python
- Java
- TypeScript
- C# (.NET)
