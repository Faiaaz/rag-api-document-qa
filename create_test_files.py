#!/usr/bin/env python3
"""
Create test files of different types for manual API testing
"""
import os
from pathlib import Path
import pandas as pd

def create_test_files():
    """Create test files of various types"""
    test_dir = Path("manual_test_files")
    test_dir.mkdir(exist_ok=True)
    
    print("📁 Creating test files in 'manual_test_files' directory...")
    
    # 1. Text file
    text_file = test_dir / "sample_text.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write("Sample Text Document\n")
        f.write("This is a sample text document for testing the RAG API.\n")
        f.write("It contains information about various topics including:\n")
        f.write("- Machine learning and artificial intelligence\n")
        f.write("- Data science and analytics\n")
        f.write("- Software development and programming\n")
        f.write("- Business strategy and management\n")
        f.write("This document will be processed and stored in the vector database.\n")
    print(f"✅ Created: {text_file}")
    
    # 2. Markdown file
    md_file = test_dir / "sample_markdown.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# Sample Markdown Document\n\n")
        f.write("## Introduction\n")
        f.write("This is a **markdown document** for testing the RAG API.\n\n")
        f.write("## Key Features\n")
        f.write("- *Italic text* and **bold text**\n")
        f.write("- Lists and bullet points\n")
        f.write("- Code blocks and formatting\n\n")
        f.write("## Technical Content\n")
        f.write("The document discusses:\n")
        f.write("1. API development with FastAPI\n")
        f.write("2. Vector databases and embeddings\n")
        f.write("3. Natural language processing\n")
        f.write("4. Machine learning applications\n")
    print(f"✅ Created: {md_file}")
    
    # 3. CSV file
    csv_file = test_dir / "sample_data.csv"
    data = {
        'Product': ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard'],
        'Category': ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics'],
        'Price': [1200, 800, 500, 300, 100],
        'Description': [
            'High-performance laptop for professionals',
            'Smartphone with advanced features',
            'Portable tablet for entertainment',
            'Large monitor for productivity',
            'Mechanical keyboard for gaming'
        ]
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    print(f"✅ Created: {csv_file}")
    
    # 4. JSON file
    json_file = test_dir / "sample_config.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write('{\n')
        f.write('  "application": "RAG API Test",\n')
        f.write('  "version": "1.0.0",\n')
        f.write('  "features": [\n')
        f.write('    "Document processing",\n')
        f.write('    "Vector search",\n')
        f.write('    "Question answering",\n')
        f.write('    "OCR support"\n')
        f.write('  ],\n')
        f.write('  "settings": {\n')
        f.write('    "chunk_size": 1000,\n')
        f.write('    "embedding_model": "all-MiniLM-L6-v2",\n')
        f.write('    "llm_model": "gpt-3.5-turbo"\n')
        f.write('  }\n')
        f.write('}\n')
    print(f"✅ Created: {json_file}")
    
    # 5. HTML file
    html_file = test_dir / "sample_webpage.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n<head>\n<title>Sample Webpage</title>\n</head>\n<body>\n')
        f.write('<h1>Sample Webpage Content</h1>\n')
        f.write('<p>This is a sample HTML webpage for testing the RAG API.</p>\n')
        f.write('<h2>Features</h2>\n')
        f.write('<ul>\n')
        f.write('<li>HTML parsing and text extraction</li>\n')
        f.write('<li>Web content processing</li>\n')
        f.write('<li>Structured data handling</li>\n')
        f.write('</ul>\n')
        f.write('<h2>Technical Information</h2>\n')
        f.write('<p>The webpage contains information about web development, HTML, CSS, and JavaScript.</p>\n')
        f.write('</body>\n</html>\n')
    print(f"✅ Created: {html_file}")
    
    # 6. Log file
    log_file = test_dir / "sample_log.log"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write('2024-01-15 10:30:15 INFO Application started\n')
        f.write('2024-01-15 10:30:16 INFO Loading configuration\n')
        f.write('2024-01-15 10:30:17 INFO Database connection established\n')
        f.write('2024-01-15 10:30:18 INFO API server running on port 8000\n')
        f.write('2024-01-15 10:30:19 INFO Document processor initialized\n')
        f.write('2024-01-15 10:30:20 INFO Vector store loaded successfully\n')
        f.write('2024-01-15 10:30:21 INFO LLM client connected\n')
        f.write('2024-01-15 10:30:22 INFO Health check passed\n')
        f.write('2024-01-15 10:30:23 INFO Ready to process requests\n')
    print(f"✅ Created: {log_file}")
    
    print(f"\n🎉 All test files created in '{test_dir}' directory!")
    print("📋 Files created:")
    for file in test_dir.glob("*"):
        print(f"   - {file.name}")
    
    return test_dir

if __name__ == "__main__":
    create_test_files() 