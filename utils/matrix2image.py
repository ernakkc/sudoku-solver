import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os


def matrix_to_image(matrix, output_path=None, cell_size=60, mode='RGB'):
    """
    Convert a 9x9 Sudoku matrix to a readable image with grid.
    
    Args:
        matrix: 9x9 numpy array or list (values 0-9, 0=empty)
        output_path: path to save the image (optional)
        cell_size: size of each Sudoku cell in pixels
        mode: 'RGB' for color image
    
    Returns:
        PIL Image object
    """
    matrix = np.array(matrix)
    
    # Sudoku should be 9x9
    if matrix.shape != (9, 9):
        raise ValueError(f"Matrix must be 9x9, got {matrix.shape}")
    
    # Image dimensions: 9 cells * cell_size + grid lines
    grid_width = 1  # Thin lines between cells
    thick_grid = 3  # Thick lines between 3x3 blocks
    
    img_size = 9 * cell_size + 8 * grid_width + 6 * thick_grid
    
    # Create white image
    image = Image.new('RGB', (img_size, img_size), color='white')
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, fallback to default if not available
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(cell_size * 0.6))
    except:
        font = ImageFont.load_default()
    
    # Draw grid and numbers
    for row in range(9):
        for col in range(9):
            # Calculate position with grid lines
            x_offset = col * (cell_size + grid_width)
            if col >= 3:
                x_offset += thick_grid * (col // 3 - 1)
            if col >= 6:
                x_offset += thick_grid
            
            y_offset = row * (cell_size + grid_width)
            if row >= 3:
                y_offset += thick_grid * (row // 3 - 1)
            if row >= 6:
                y_offset += thick_grid
            
            # Draw cell border (light gray)
            x1, y1 = x_offset, y_offset
            x2, y2 = x_offset + cell_size, y_offset + cell_size
            draw.rectangle([x1, y1, x2, y2], outline='lightgray', width=1)
            
            # Draw number if not 0 (empty cell)
            val = matrix[row, col]
            if val != 0:
                text = str(int(val))
                # Center text in cell
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = x1 + (cell_size - text_width) // 2
                text_y = y1 + (cell_size - text_height) // 2
                draw.text((text_x, text_y), text, fill='black', font=font)
    
    # Draw thick grid lines for 3x3 blocks
    for i in range(1, 3):  # 2 thick lines (3x3 blocks)
        offset = i * (3 * cell_size + 3 * grid_width) + i * thick_grid
        # Vertical line
        draw.line([(offset, 0), (offset, img_size)], fill='black', width=thick_grid)
        # Horizontal line
        draw.line([(0, offset), (img_size, offset)], fill='black', width=thick_grid)
    
    # Save if path provided
    if output_path:
        image.save(output_path)
    
    return image

if __name__ == "__main__":
    # Example: solved Sudoku
    sample_matrix = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
    os.makedirs('results', exist_ok=True)
    # cell_size=52 → 9*52 + 8 + 18 = 494x494 ≈ 500x500
    img = matrix_to_image(sample_matrix, output_path='results/sudoku_solution.png', cell_size=52)
    print("Sudoku image saved to results/sudoku_solution.png")
    img.show()
