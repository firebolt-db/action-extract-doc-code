import argparse
import os
import re
from typing import Dict, List, Optional, Union


def extract_code_blocks(markdown_content: str, language: str) -> List[str]:
    """Extract code blocks of a specific language from markdown content."""
    pattern = re.compile(f"```{language}(.*?)```", re.DOTALL)
    return pattern.findall(markdown_content)


def read_markdown_file(file_path: str) -> Optional[str]:
    """Read content from a markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def write_single_block(block: str, output_file: str) -> bool:
    """Write a single code block to an output file."""
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        with open(output_file, "w", encoding="utf-8") as out_file:
            out_file.write(block.strip())
        return True
    except Exception as e:
        print(f"Error writing to output file: {e}")
        return False


def write_all_blocks(blocks: List[str], base_output_file: str) -> Dict[int, str]:
    """
    Write all code blocks to separate files with numbering.
    Returns a dictionary mapping block numbers to their output files.
    """
    if not blocks:
        return {}
    
    # Split the filename and extension
    file_path, file_ext = os.path.splitext(base_output_file)
    
    output_files = {}
    
    for i, block in enumerate(blocks, 1):
        output_file = f"{file_path}_block_{i}{file_ext}"
        if write_single_block(block, output_file):
            output_files[i] = output_file
    
    return output_files


def write_output_file(blocks: List[str], output_file: str, block_number: Optional[int] = None) -> Union[bool, Dict[int, str]]:
    """
    Write extracted code blocks to output file(s).
    If block_number is specified, only that block is written to the output file.
    Otherwise, all blocks are written to separate files.
    """
    if not blocks:
        return False
    
    if block_number is not None:
        if 1 <= block_number <= len(blocks):
            return write_single_block(blocks[block_number-1], output_file)
        else:
            print(f"Error: Block number {block_number} is out of range. Found {len(blocks)} blocks.")
            return False
    else:
        return write_all_blocks(blocks, output_file)


def main():
    """Main function to process command line arguments and extract code."""
    parser = argparse.ArgumentParser(description='Extract code blocks from markdown files.')
    parser.add_argument('--input', '-i', required=True, help='Input markdown file path')
    parser.add_argument('--output', '-o', help='Output file path (default: extracted_<language>[_block_<n>].extension)')
    parser.add_argument('--language', '-l', default='javascript', help='Language of code blocks to extract (default: javascript)')
    parser.add_argument('--block', '-b', type=int, help='Specific block number to extract (1-indexed)')
    
    args = parser.parse_args()
    
    # Determine output file extension based on language
    extension_map = {
        'javascript': 'ts', # We're using TypeScript for JavaScript code in docs
        'python': 'py',
        'java': 'java',
        'typescript': 'ts',
        'dotnet': 'cs',
    }
    
    # Get file extension for the language
    lang_extension = extension_map.get(args.language, args.language)
    
    # Set default output file if not provided
    if not args.output:
        input_dir = os.path.dirname(args.input)
        input_name = os.path.splitext(os.path.basename(args.input))[0]
        args.output = os.path.join(input_dir, f"extracted_{input_name}_{args.language}.{lang_extension}")
    
    # Read the markdown content
    content = read_markdown_file(args.input)
    if content is None:
        return
    
    # Extract code blocks
    code_blocks = extract_code_blocks(content, args.language)
    
    if not code_blocks:
        print(f"No {args.language} code blocks found in {args.input}")
        return
    
    # Write extracted code to output file(s)
    result = write_output_file(code_blocks, args.output, args.block)
    
    if isinstance(result, dict):
        print(f"Found {len(result)} {args.language} code blocks:")
        for block_num, file_path in result.items():
            print(f"  Block {block_num} extracted to {file_path}")
    elif result:
        if args.block:
            print(f"{args.language} code block {args.block} extracted to {args.output}")
        else:
            print(f"{args.language} code block extracted to {args.output}")
    else:
        if args.block:
            print(f"Failed to extract {args.language} code block {args.block}")
        else:
            print(f"Failed to extract {args.language} code blocks")


if __name__ == "__main__":
    main()