import cv2
import numpy as np
import os
import time
from datetime import datetime


class ImagePreprocessor:    
    def __init__(self, save_steps=True, output_dir="preprocessing_steps", update_callback=None):
        self.save_steps = save_steps
        self.output_dir = output_dir
        self.update_callback = update_callback 
        self.steps = [] 
        
        if save_steps:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.session_dir = os.path.join(output_dir, timestamp)
            os.makedirs(self.session_dir, exist_ok=True)
    
    def _save_step(self, image, step_name):
        if self.save_steps:
            filename = f"{len(self.steps)+1:02d}_{step_name}.png"
            filepath = os.path.join(self.session_dir, filename)
            cv2.imwrite(filepath, image)
            self.steps.append((step_name, filepath))
            
            if self.update_callback:
                self.update_callback(filepath)
                time.sleep(0.5)
            
            return filepath
        return None
    
    def preprocess(self, image_path):
        # Step 1: Original Image
        original = cv2.imread(image_path)
        if original is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        self._save_step(original, "01_original")
        
        # Step 2: Grayscale
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        self._save_step(gray, "02_grayscale")
        
        # Step 3: Normalize brightness 
        normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        self._save_step(normalized, "03_normalized")
        
        # Step 4: CLAHE 
        # Kontrast iyileştirmesi çizgileri daha belirgin yapar
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_enhanced = clahe.apply(normalized)
        self._save_step(contrast_enhanced, "04_contrast_enhanced")
        
        # Step 5: Gaussian blur
        blurred = cv2.GaussianBlur(contrast_enhanced, (3, 3), 0)
        self._save_step(blurred, "05_light_blur")
        
        # Step 6: Canny edge for find contours 
        edges = cv2.Canny(blurred, 50, 150)
        self._save_step(edges, "06_canny_edges")
        
        # Step 7: connect broken lines 
        kernel_dilate_early = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated_edges = cv2.dilate(edges, kernel_dilate_early, iterations=1)
        self._save_step(dilated_edges, "07_dilated_edges")
        
        # Step 8: Find contours from edges
        contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw contours on a copy for visualization
        contour_img = original.copy()
        cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
        self._save_step(contour_img, "08_contours_detected")
        
        # Step 9: Find the outermost rectangle (largest contour)
        if contours and len(contours) > 0:
            # Sort contours by area (largest first)
            contours_sorted = sorted(contours, key=cv2.contourArea, reverse=True)
            
            # Take the largest contour as the outermost rectangle
            largest_contour = contours_sorted[0]
            largest_area = cv2.contourArea(largest_contour)
            
            # Draw the largest contour
            largest_contour_img = original.copy()
            cv2.drawContours(largest_contour_img, [largest_contour], -1, (0, 255, 0), 3)
            self._save_step(largest_contour_img, "09_largest_contour")
            
            # Step 10: Get bounding box and crop
            x, y, w, h = cv2.boundingRect(largest_contour)
            cropped = blurred[y:y+h, x:x+w]
            self._save_step(cropped, "10_cropped")
            
            # Step 11: Resize to standard size (500x500)
            resized = cv2.resize(cropped, (500, 500), interpolation=cv2.INTER_CUBIC)
            self._save_step(resized, "11_resized")
            
            # Step 12: Re-normalize after cropping
            resized_normalized = cv2.normalize(resized, None, 0, 255, cv2.NORM_MINMAX)
            self._save_step(resized_normalized, "12_resized_normalized")
            
            # Step 13: CLAHE for better contrast
            resized_clahe = clahe.apply(resized_normalized)
            self._save_step(resized_clahe, "13_resized_contrast_enhanced")
            
            # Step 14: Adaptive threshold
            final_thresh = cv2.adaptiveThreshold(
                resized_clahe, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                23, 8  
            )
            self._save_step(final_thresh, "14_adaptive_threshold")
            
            # Step 15: Check if image needs inversion 
            # Count white vs black pixels to decide
            white_pixels = np.sum(final_thresh == 255)
            black_pixels = np.sum(final_thresh == 0)
            
            if white_pixels > black_pixels:
                final = cv2.bitwise_not(final_thresh)
                self._save_step(final, "15_inverted_final_result")
            else:
                final = final_thresh
                self._save_step(final, "15_final_result")
            
            return final, self.steps
        else:
            self._save_step(original, "09_no_contours_using_full_image")
            resized = cv2.resize(blurred, (500, 500), interpolation=cv2.INTER_CUBIC)
            self._save_step(resized, "10_full_image_resized")
            resized_normalized = cv2.normalize(resized, None, 0, 255, cv2.NORM_MINMAX)
            self._save_step(resized_normalized, "11_normalized")
            
            _, fallback_thresh = cv2.threshold(resized_normalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            self._save_step(fallback_thresh, "12_fallback_threshold")
            
            return fallback_thresh, self.steps


def preprocess_sudoku_image(image_path, save_steps=True, output_dir="preprocessing_steps", update_callback=None):
    preprocessor = ImagePreprocessor(save_steps=save_steps, output_dir=output_dir, update_callback=update_callback)
    return preprocessor.preprocess(image_path)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "../sudoku_examples/sudoku1.png"
    
    print(f"Processing: {image_path}")
    processed, steps = preprocess_sudoku_image(image_path)
    
    print(f"\nPreprocessing complete! {len(steps)} steps saved:")
    for step_name, step_path in steps:
        print(f"  - {step_name}: {step_path}")
    
    print(f"\nFinal image shape: {processed.shape}")
