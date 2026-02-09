"""
Test script for ESP column detection functionality.
Run this to verify the ESP detection logic works correctly.
"""

import pandas as pd
import io
from main import detect_esp_column, DetectionConfidence


def test_high_confidence():
    """Test case: Single ESP column match (high confidence)"""
    print("\n=== Test 1: High Confidence (Single Match) ===")
    
    df = pd.DataFrame({
        'Email': ['test1@example.com', 'test2@example.com'],
        'ESP': ['Gmail', 'Yahoo'],
        'Name': ['John Doe', 'Jane Smith']
    })
    
    result = detect_esp_column(df)
    
    print(f"Confidence: {result.confidence}")
    print(f"Detected Column: {result.detected_column}")
    print(f"Candidates: {result.candidates}")
    
    assert result.confidence == DetectionConfidence.HIGH
    assert result.detected_column == 'ESP'
    assert len(result.candidates) == 1
    print("✓ Test passed!")


def test_case_insensitive():
    """Test case: Case-insensitive matching"""
    print("\n=== Test 2: Case-Insensitive Matching ===")
    
    df = pd.DataFrame({
        'Email': ['test1@example.com'],
        'email service provider': ['Gmail'],
        'Name': ['John Doe']
    })
    
    result = detect_esp_column(df)
    
    print(f"Confidence: {result.confidence}")
    print(f"Detected Column: {result.detected_column}")
    
    assert result.confidence == DetectionConfidence.HIGH
    assert result.detected_column == 'email service provider'
    print("✓ Test passed!")


def test_whitespace_trimming():
    """Test case: Whitespace trimming"""
    print("\n=== Test 3: Whitespace Trimming ===")
    
    df = pd.DataFrame({
        'Email': ['test1@example.com'],
        '  Provider  ': ['Gmail'],
        'Name': ['John Doe']
    })
    
    result = detect_esp_column(df)
    
    print(f"Confidence: {result.confidence}")
    print(f"Detected Column: {result.detected_column}")
    
    assert result.confidence == DetectionConfidence.HIGH
    assert result.detected_column == '  Provider  '
    print("✓ Test passed!")


def test_low_confidence():
    """Test case: Multiple matches (low confidence)"""
    print("\n=== Test 4: Low Confidence (Multiple Matches) ===")
    
    df = pd.DataFrame({
        'Email': ['test1@example.com'],
        'ESP': ['Gmail'],
        'Provider': ['Google'],
        'Name': ['John Doe']
    })
    
    result = detect_esp_column(df)
    
    print(f"Confidence: {result.confidence}")
    print(f"Detected Column: {result.detected_column}")
    print(f"Candidates: {result.candidates}")
    print(f"Preview data provided: {result.preview_data is not None}")
    
    assert result.confidence == DetectionConfidence.LOW
    assert result.detected_column is None
    assert len(result.candidates) == 2
    assert result.preview_data is not None
    print("✓ Test passed!")


def test_no_confidence():
    """Test case: No matches (no confidence)"""
    print("\n=== Test 5: No Confidence (No Matches) ===")
    
    df = pd.DataFrame({
        'Email': ['test1@example.com'],
        'Company': ['Google'],
        'Name': ['John Doe']
    })
    
    result = detect_esp_column(df)
    
    print(f"Confidence: {result.confidence}")
    print(f"Detected Column: {result.detected_column}")
    print(f"Candidates (all columns): {result.candidates}")
    print(f"Preview data provided: {result.preview_data is not None}")
    
    assert result.confidence == DetectionConfidence.NONE
    assert result.detected_column is None
    assert len(result.candidates) == 3  # All columns
    assert result.preview_data is not None
    print("✓ Test passed!")


def test_all_variants():
    """Test case: All common ESP column name variants"""
    print("\n=== Test 6: All ESP Variants Recognition ===")
    
    variants = [
        'esp',
        'ESP',
        'email service provider',
        'Email Service Provider',
        'EMAIL SERVICE PROVIDER',
        'email provider',
        'Email Provider',
        'provider',
        'Provider',
        'PROVIDER',
        'mail provider',
        'Mail Provider',
    ]
    
    for variant in variants:
        df = pd.DataFrame({
            'Email': ['test@example.com'],
            variant: ['Gmail'],
            'Name': ['John Doe']
        })
        
        result = detect_esp_column(df)
        
        assert result.confidence == DetectionConfidence.HIGH, f"Failed for variant: {variant}"
        assert result.detected_column == variant, f"Wrong column detected for variant: {variant}"
        print(f"✓ Variant '{variant}' detected successfully")
    
    print("✓ All variants test passed!")


def test_large_dataset():
    """Test case: Large dataset (1000+ rows)"""
    print("\n=== Test 7: Large Dataset ===")
    
    data = {
        'Email': [f'user{i}@example.com' for i in range(1000)],
        'ESP': ['Gmail'] * 500 + ['Yahoo'] * 500,
        'Name': [f'User {i}' for i in range(1000)]
    }
    df = pd.DataFrame(data)
    
    result = detect_esp_column(df)
    
    print(f"Confidence: {result.confidence}")
    print(f"Detected Column: {result.detected_column}")
    print(f"Total rows: {result.total_rows}")
    
    assert result.confidence == DetectionConfidence.HIGH
    assert result.detected_column == 'ESP'
    assert result.total_rows == 1000
    print("✓ Test passed!")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("ESP COLUMN DETECTION TESTS")
    print("=" * 60)
    
    try:
        test_high_confidence()
        test_case_insensitive()
        test_whitespace_trimming()
        test_low_confidence()
        test_no_confidence()
        test_all_variants()
        test_large_dataset()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        raise
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
