"""
Text matching utilities for transcription analysis without NLTK dependency
"""

import re
import numpy as np
from difflib import SequenceMatcher

def preprocess_text(text):
    """
    Basic text preprocessing - lowercase, remove punctuation, normalize spaces
    """
    text = text.lower()
    # Remove punctuation and normalize whitespace
    text = re.sub(r'[.,!?-]', ' ', text)
    text = ' '.join(text.split())
    return text

def get_context_score(text, words_before, words_after):
    """
    Calculate context relevance score based on surrounding words
    
    Args:
        text: Original text
        words_before: List of words before match
        words_after: List of words after match
        
    Returns:
        float: Context score between 0-1
    """
    emphasis_words = {
        'important', 'key', 'main', 'significant', 'essential',
        'fundamental', 'crucial', 'vital', 'core', 'primary',
        'major', 'central', 'notably', 'specifically', 'particularly'
    }
    
    transition_words = {
        'however', 'moreover', 'therefore', 'consequently',
        'indeed', 'notably', 'example', 'instance', 'like',
        'such as', 'similar to', 'including'
    }
    
    surrounding_words = words_before + words_after
    
    # Score based on emphasis words
    emphasis_count = sum(1 for word in surrounding_words if word in emphasis_words)
    emphasis_score = emphasis_count / max(len(surrounding_words), 1)
    
    # Score based on transition words
    transition_count = sum(1 for word in surrounding_words if word in transition_words)
    transition_score = transition_count / max(len(surrounding_words), 1)
    
    # Position score - prefer matches with words on both sides
    position_score = 1.0 if words_before and words_after else 0.5
    
    # Combine scores
    total_score = (0.4 * emphasis_score + 
                  0.3 * transition_score + 
                  0.3 * position_score)
    
    return min(1.0, total_score)

def get_fuzzy_match_score(str1, str2):
    """
    Get similarity score between two strings
    
    Returns:
        float: Similarity score between 0 and 100
    """
    str1 = preprocess_text(str1)
    str2 = preprocess_text(str2)
    
    # First try exact substring matching
    if str1 in str2 or str2 in str1:
        return 100.0
        
    # Use SequenceMatcher for fuzzy matching
    ratio = SequenceMatcher(None, str1, str2).ratio() * 100
    
    # Check partial word matches
    words1 = set(str1.split())
    words2 = set(str2.split())
    common_words = words1.intersection(words2)
    
    if common_words:
        word_match_ratio = len(common_words) / max(len(words1), len(words2)) * 100
        ratio = max(ratio, word_match_ratio * 0.8)  # Weight partial matches slightly lower
        
    return ratio

def find_best_fuzzy_match(text, markers, threshold=85):
    """
    Find best matching marker phrase with context consideration
    
    Args:
        text (str): Text to search in
        markers (list): List of marker phrases to look for
        threshold (float): Minimum similarity score (0-100)
        
    Returns:
        tuple: (matched_phrase, similarity_score, context_score)
    """
    text = preprocess_text(text)
    words = text.split()
    
    best_score = 0
    best_match = None
    best_context = 0
    
    # Try each marker
    for marker in markers:
        marker = preprocess_text(marker)
        marker_words = marker.split()
        marker_len = len(marker_words)
        
        # Slide through text words with overlap
        for i in range(len(words) - marker_len + 1):
            # Get current window of words
            window = ' '.join(words[i:i + marker_len + 1])  # +1 for flexibility
            
            # Calculate match score
            score = get_fuzzy_match_score(marker, window)
            
            if score >= threshold:
                # Calculate context score using surrounding words
                words_before = words[max(0, i-5):i]
                words_after = words[i+marker_len:i+marker_len+5]
                context_score = get_context_score(text, words_before, words_after)
                
                # Combine scores with weights
                final_score = 0.7 * score + 0.3 * (context_score * 100)
                
                if final_score > best_score:
                    best_score = final_score
                    best_match = marker
                    best_context = context_score
    
    if best_score >= threshold:
        return best_match, best_score, best_context
        
    return None, 0, 0

def normalize_scores(scores):
    """
    Normalize scores to mean=0, std=1 for comparison with audio scores
    """
    if not scores:
        return scores
    scores = np.array(scores)
    mean = np.mean(scores)
    std = np.std(scores)
    if std == 0:
        return scores - mean
    return (scores - mean) / std