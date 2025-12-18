import cv2
import numpy as np
from PIL import Image
import random

def analyze_image(image_path):
    """
    Analyze uploaded image for skin type and concerns.
    Returns recommendations based on image analysis.
    """
    try:
        # Load image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            # Fallback if OpenCV fails - use PIL
            img_pil = Image.open(image_path)
            img_array = np.array(img_pil)
            img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Convert to HSV for better color analysis
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Detect skin tones (simplified approach)
        # Skin tone ranges in HSV: H (0-20, 170-180), S (20-40), V (70-255)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 40, 255], dtype=np.uint8)
        skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Also check for extended skin tone range
        lower_skin2 = np.array([170, 20, 70], dtype=np.uint8)
        upper_skin2 = np.array([180, 40, 255], dtype=np.uint8)
        skin_mask2 = cv2.inRange(hsv, lower_skin2, upper_skin2)
        skin_mask = cv2.bitwise_or(skin_mask, skin_mask2)
        
        # Analyze brightness and saturation for skin type determination
        brightness = np.mean(hsv[:, :, 2])
        saturation = np.mean(hsv[:, :, 1])
        
        # Determine skin type based on analysis
        if saturation > 100 and brightness < 100:
            skin_type = 'oily'
        elif saturation < 50 and brightness < 80:
            skin_type = 'dry'
        elif saturation > 80:
            skin_type = 'combination'
        elif brightness < 70:
            skin_type = 'sensitive'
        else:
            skin_type = 'normal'
        
        # Detect concerns based on brightness and texture
        concerns = []
        
        # Check for potential acne/blemishes (dark spots)
        if brightness < 90:
            concerns.append('possible acne-prone areas')
        
        # Check for dry patches (high variance)
        variance = np.var(hsv[:, :, 2])
        if variance > 2000:
            concerns.append('visible texture variation')
        
        # Check for oiliness (high saturation)
        if saturation > 110:
            concerns.append('excess oiliness')
        
        if not concerns:
            concerns.append('minimal visible concerns')
        
        concerns_text = ', '.join(concerns)
        
        # Recommendations based on skin type
        recommendations = {
            'oily': {
                'skincare': [
                    'Oil-free gel cleanser',
                    'Salicylic acid toner',
                    'Niacinamide serum',
                    'Lightweight gel moisturizer',
                    'Oil-control primer'
                ],
                'makeup': [
                    'Matte foundation',
                    'Oil-control primer',
                    'Powder blush',
                    'Matte concealer',
                    'Bronzing powder'
                ]
            },
            'dry': {
                'skincare': [
                    'Gentle cream cleanser',
                    'Hydrating toner',
                    'Hyaluronic acid serum',
                    'Rich moisturizer',
                    'Face oil'
                ],
                'makeup': [
                    'Dewy foundation',
                    'Hydrating primer',
                    'Cream blush',
                    'Luminous concealer',
                    'Highlighting powder'
                ]
            },
            'combination': {
                'skincare': [
                    'Balanced cleanser',
                    'Balancing toner',
                    'Lightweight hydrating serum',
                    'Gel-cream moisturizer',
                    'Zone-specific treatments'
                ],
                'makeup': [
                    'Balanced foundation',
                    'Multi-purpose primer',
                    'Cream-powder blush',
                    'Universal concealer',
                    'Balancing powder'
                ]
            },
            'normal': {
                'skincare': [
                    'Mild cleanser',
                    'Regular toner',
                    'Hydrating serum',
                    'Daily moisturizer',
                    'Sunscreen SPF 30+'
                ],
                'makeup': [
                    'Natural foundation',
                    'Light primer',
                    'Natural blush',
                    'Universal concealer',
                    'Finishing powder'
                ]
            },
            'sensitive': {
                'skincare': [
                    'Hypoallergenic cleanser',
                    'Soothing toner',
                    'Calming serum',
                    'Gentle moisturizer',
                    'Barrier repair cream'
                ],
                'makeup': [
                    'Hypoallergenic foundation',
                    'Sensitive skin primer',
                    'Natural blush',
                    'Gentle concealer',
                    'Soft powder'
                ]
            }
        }
        
        recs = recommendations.get(skin_type, recommendations['normal'])
        
        return {
            "skin_type": skin_type.lower(),
            "concerns": concerns_text,
            "skincare": recs['skincare'],
            "makeup": recs['makeup']
        }
    
    except Exception as e:
        # Fallback to default if analysis fails
        print(f"Image analysis error: {e}")
        return {
            "skin_type": random.choice(['oily', 'dry', 'combination', 'normal']).lower(),
            "concerns": "Unable to analyze - please try again with better lighting",
            "skincare": [
                "Gentle cleanser",
                "Hydrating serum",
                "Moisturizer"
            ],
            "makeup": [
                "Foundation",
                "Concealer",
                "Blush"
            ]
        }
