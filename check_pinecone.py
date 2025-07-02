#!/usr/bin/env python3
"""
Debug script to check Pinecone index configuration
"""

import os
from src.utils import load_keys
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Load keys
keys = load_keys()
pinecone_key = keys.get("pinecone", "")

if not pinecone_key:
    print("❌ No Pinecone API key found")
    exit(1)

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_key)

# Check existing indexes
print("🔍 Checking Pinecone indexes...")
indexes = pc.list_indexes()
print(f"Found indexes: {[idx.name for idx in indexes]}")

# Check indianconsti index
try:
    index = pc.Index("indianconsti")
    stats = index.describe_index_stats()
    print(f"\n📊 Index 'indianconsti' stats:")
    print(f"  - Total vectors: {stats.get('total_vector_count', 0)}")
    print(f"  - Dimension: {stats.get('dimension', 'unknown')}")
    print(f"  - Namespaces: {stats.get('namespaces', {})}")
    
    # Get index info
    index_info = pc.describe_index("indianconsti")
    print(f"\n📋 Index configuration:")
    print(f"  - Dimension: {index_info.dimension}")
    print(f"  - Metric: {index_info.metric}")
    print(f"  - Host: {index_info.host}")
    
    # Check embedding model dimensions
    print(f"\n🤖 Checking embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    test_embedding = model.encode(["test"])
    print(f"  - Model output dimension: {len(test_embedding[0])}")
    
    if index_info.dimension != len(test_embedding[0]):
        print(f"\n❌ DIMENSION MISMATCH!")
        print(f"  - Index expects: {index_info.dimension} dimensions")
        print(f"  - Model outputs: {len(test_embedding[0])} dimensions")
        print(f"\n🔧 Solution: Delete and recreate the index with {len(test_embedding[0])} dimensions")
    else:
        print(f"\n✅ Dimensions match!")
        
        # Try a test query
        print("\n🧪 Testing search...")
        results = index.query(
            vector=test_embedding[0].tolist(),
            top_k=5,
            include_metadata=True
        )
        print(f"Found {len(results['matches'])} results")
        for i, match in enumerate(results['matches'][:3]):
            print(f"\nResult {i+1}:")
            print(f"  - Score: {match['score']}")
            print(f"  - ID: {match['id']}")
            if 'metadata' in match and 'text' in match['metadata']:
                print(f"  - Text preview: {match['metadata']['text'][:100]}...")
    
except Exception as e:
    print(f"❌ Error accessing index: {e}")