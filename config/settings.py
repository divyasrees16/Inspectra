from pathlib import Path

# ==== Config ====
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
YOLO_ONNX_PATH = str(MODEL_DIR / "best.onnx")
EFFNET_ONNX_PATH = str(MODEL_DIR / "effnet_gc10.onnx")
CLASS_NAMES = ['crease', 'crescent_gap', 'inclusion', 'oil_spot', 'punching_hole',
               'rolled_pit', 'silk_spot', 'waist_folding', 'water_spot', 'welding_line']
CLASS_NAMES_YOLO = ['crease', 'crescent_gap', 'inclusion', 'oil_spot', 'punching_hole',
                    'silk_spot', 'waist_folding', 'water_spot', 'welding_line']

# Defect descriptions for context
DEFECT_DESCRIPTIONS = {
    'crease': 'A fold or wrinkle in the metal surface, typically caused by improper handling or processing',
    'crescent_gap': 'A curved gap or opening in the material, often indicating structural weakness',
    'inclusion': 'Foreign material embedded in the metal, which can compromise structural integrity',
    'oil_spot': 'Staining or discoloration caused by oil contamination during manufacturing',
    'punching_hole': 'Unwanted holes created during the punching or forming process',
    'rolled_pit': 'Small depressions or cavities formed during the rolling process',
    'silk_spot': 'Surface irregularities with a silk-like appearance, indicating material inconsistency',
    'waist_folding': 'Folding defects that occur at the waist or narrow sections of the material',
    'water_spot': 'Staining or corrosion marks caused by water exposure',
    'welding_line': 'Visible lines or marks from welding operations, which may indicate quality issues'
}