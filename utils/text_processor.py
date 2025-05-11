"""
Text processing utilities for the script generator.
"""

def split_into_segments(text: str, segment_size: int = 500) -> list:
    """
    Split text into segments of specified size.
    
    Args:
        text (str): The text to split
        segment_size (int): Size of each segment in words
        
    Returns:
        list: List of text segments
    """
    words = text.split()
    segments = []
    
    for i in range(0, len(words), segment_size):
        segment = ' '.join(words[i:i + segment_size])
        segments.append(segment)
    
    return segments

def count_words(text: str) -> int:
    """
    Count the number of words in a text.
    
    Args:
        text (str): The text to count words in
        
    Returns:
        int: Number of words
    """
    return len(text.split())

def insert_ctas(text: str, word_count: int) -> str:
    """
    Insert CTAs at appropriate positions in the text.
    
    Args:
        text (str): The text to insert CTAs into
        word_count (int): Total word count of the text
        
    Returns:
        str: Text with CTAs inserted
    """
    # First CTA after intro (20-40 seconds)
    intro_cta = "Before we jump back in, tell us where you're tuning in from, and if this story touches you, make sure you're subscribed—because tomorrow, I've saved something extra special for you!"
    
    # Second CTA around 1,500 words
    mid_cta = "Preparing and narrating this story took us a lot of time, so if you are enjoying it, subscribe to our channel, it means a lot to us! Now back to the story."
    
    # Third CTA around 40 minutes
    late_cta = "Enjoying the video so far? Don't forget to subscribe!"
    
    # Final CTA at the end
    final_cta = "Up next, you've got two more standout stories right on your screen. If this one hit the mark, you won't want to pass these up. Just click and check them out! And don't forget to subscribe and turn on the notification bell, so you don't miss any upload from us!"
    
    # Split text into paragraphs
    paragraphs = text.split('\n\n')
    
    # Insert CTAs at appropriate positions
    if len(paragraphs) > 2:
        paragraphs.insert(2, intro_cta)
    
    mid_point = int(len(paragraphs) * 0.3)  # Approximately 1,500 words
    if mid_point < len(paragraphs):
        paragraphs.insert(mid_point, mid_cta)
    
    late_point = int(len(paragraphs) * 0.7)  # Approximately 40 minutes
    if late_point < len(paragraphs):
        paragraphs.insert(late_point, late_cta)
    
    # Add final CTA
    paragraphs.append(final_cta)
    
    return '\n\n'.join(paragraphs) 