from google import genai
from google.genai import types
from configparser import ConfigParser
import re


def validate_matrix(matrix):
    if not matrix or len(matrix) != 9:
        return False, f"Matrix must have 9 rows, found {len(matrix) if matrix else 0}"
    
    for i, row in enumerate(matrix):
        if len(row) != 9:
            return False, f"Row {i+1} must have 9 columns, found {len(row)}"
        
        for j, val in enumerate(row):
            if not isinstance(val, int) or val < 0 or val > 9:
                return False, f"Invalid value at row {i+1}, col {j+1}: {val} (must be 0-9)"
    
    return True, None


def with_gemini(API_KEY: str, image_path: str, max_retries=3):
    image_bytes = open(image_path, "rb").read()
    client = genai.Client(api_key=API_KEY)
    
    prompt = """You are analyzing a preprocessed Sudoku puzzle image. Your task is to extract the 9x9 grid with PERFECT ACCURACY.

IMPORTANT INSTRUCTIONS:
1. Look at each cell carefully - distinguish between EMPTY (0) and FILLED (1-9) cells
2. Empty cells might appear as white/blank spaces - mark these as 0
3. For filled cells, read the digit carefully (1,2,3,4,5,6,7,8,9)
4. The grid MUST be exactly 9 rows by 9 columns
5. Scan LEFT-TO-RIGHT, TOP-TO-BOTTOM

CRITICAL FORMATTING REQUIREMENTS:
- Each row MUST be on a separate line
- Use integers 1-9 for filled cells, 0 for EMPTY cells
- Output exactly 9 rows, each containing exactly 9 integers
- NO markdown, NO code blocks, NO explanations, NO extra text
- Start with [[ and end with ]]

EXACT OUTPUT FORMAT (each row on new line):
[[5,3,0,0,7,0,0,0,0],
[6,0,0,1,9,5,0,0,0],
[0,9,8,0,0,0,0,6,0],
[8,0,0,0,6,0,0,0,3],
[4,0,0,8,0,3,0,0,1],
[7,0,0,0,2,0,0,0,6],
[0,6,0,0,0,0,2,8,0],
[0,0,0,4,1,9,0,0,5],
[0,0,0,0,8,0,0,7,9]]

Double-check:
- Empty/blank cells = 0
- Numbers in cells = actual digit (1-9)
- Exactly 9 rows, 9 columns

Respond with this format only, no other text."""
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content( 
                model='gemini-2.5-flash',
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type='image/png',
                    ),
                    prompt
                ],
            )
            
            output = response.text
            cleaned_output = output.replace('```json', '').replace('```python', '').replace('```', '').strip()
            
            # Parse matrix
            matrix = []
            for i, line in enumerate(cleaned_output.splitlines()):
                if line == '[' or line == ']':
                    continue
                line = line.replace(' ',"").replace('[', '').replace(']', '')
                if not line or line == ',':
                    continue
                    
                row = []
                for num in line.split(','):
                    if num:
                        try:
                            row.append(int(num))
                        except ValueError:
                            continue
                
                if row:
                    matrix.append(row)
            
            # Validate
            is_valid, error_msg = validate_matrix(matrix)
            
            if is_valid:
                print(f"[Gemini] Successfully extracted matrix on attempt {attempt + 1}")
                return matrix
            else:
                print(f"[Gemini] Attempt {attempt + 1} failed validation: {error_msg}")
                if attempt < max_retries - 1:
                    print(f"[Gemini] Retrying...")
                    continue
        
        except Exception as e:
            print(f"[Gemini] Attempt {attempt + 1} failed with error: {str(e)}")
            if attempt < max_retries - 1:
                print(f"[Gemini] Retrying...")
                continue
    
    print(f"[Gemini] Failed to extract valid matrix after {max_retries} attempts")
    return None










if __name__ == "__main__":
    config = ConfigParser()
    config.read('config.ini')
    API_KEY = config.get('GENAI', 'API_KEY')
    image_path = "sudoku_examples/sudoku1.png"
    matrix = with_gemini(API_KEY, image_path)
    for row in matrix:
        print(row)
    print("Done")
