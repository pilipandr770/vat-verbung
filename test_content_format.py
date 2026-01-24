#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test improved content format
"""

import os
from dotenv import load_dotenv
load_dotenv()

from core.content_generator import ContentGenerator

def test_content_format():
    """Test the improved content format."""
    
    print("🧪 Testing Improved Content Format")
    print("=" * 40)
    
    generator = ContentGenerator()
    
    # Generate several posts to see the format
    for i in range(3):
        content = generator.generate_content()
        print(f"\n📄 Пост #{i+1}:")
        print(f"Заголовок: {content['title']}")
        print(f"Описание: {content['description']}")
        print(f"Тема: {content['theme']}")
        print("-" * 50)

if __name__ == "__main__":
    test_content_format()