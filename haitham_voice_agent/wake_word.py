"""
Wake Word Detection for HVA
Detects "هيثم" or "Haitham" in transcribed text
"""

import re


class WakeWordDetector:
    def __init__(self):
        # Wake words in different forms
        self.wake_words = [
            'هيثم',
            'haitham',
            'haithem',
            'haytham',
            'haythem',
        ]
        
    def detect(self, text):
        """
        Detect wake word in text and extract command
        Returns: (detected: bool, command: str)
        """
        if not text:
            return False, ""
        
        text_lower = text.lower().strip()
        
        # Check each wake word
        for wake_word in self.wake_words:
            # Pattern: wake_word followed by optional punctuation and command
            patterns = [
                f"{wake_word}[،,.:؛]?\\s+(.+)",  # "هيثم، احفظ ملاحظة"
                f"{wake_word}\\s+(.+)",           # "هيثم احفظ ملاحظة"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text_lower, re.IGNORECASE)
                if match:
                    command = match.group(1).strip()
                    return True, command
        
        # If no wake word found, return the whole text as command
        # (for backward compatibility)
        return False, text
    
    def has_wake_word(self, text):
        """Check if text contains wake word"""
        detected, _ = self.detect(text)
        return detected


# Singleton instance
_detector_instance = None

def get_detector():
    """Get or create the singleton detector instance"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = WakeWordDetector()
    return _detector_instance


if __name__ == "__main__":
    # Test the detector
    detector = get_detector()
    
    test_cases = [
        "هيثم، احفظ ملاحظة عن الاجتماع",
        "هيثم احفظ ملاحظة",
        "Haitham, save a note",
        "احفظ ملاحظة",  # No wake word
    ]
    
    for test in test_cases:
        detected, command = detector.detect(test)
        print(f"Input: {test}")
        print(f"Detected: {detected}, Command: {command}")
        print()
