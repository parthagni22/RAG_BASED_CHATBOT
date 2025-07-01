#!/usr/bin/env python3
"""
Create sample academic data for testing the RAG chatbot
This creates sample course information as text files that can be processed
"""

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def create_sample_pdf_content():
    """Create sample academic content"""
    
    sample_courses = [
        {
            "title": "CSCE 629 - Analysis of Algorithms",
            "content": """
            CSCE 629 - Analysis of Algorithms (3 credit hours)
            
            Prerequisites: CSCE 221 (Data Structures & Algorithms) and CSCE 222 (Discrete Structures)
            
            Course Description:
            Advanced study of algorithms and their analysis. Topics include asymptotic analysis, 
            divide-and-conquer algorithms, dynamic programming, greedy algorithms, graph algorithms, 
            network flows, linear programming, NP-completeness, and approximation algorithms.
            
            Learning Objectives:
            - Analyze the time and space complexity of algorithms
            - Design efficient algorithms for computational problems
            - Understand advanced algorithmic techniques
            - Apply mathematical tools for algorithm analysis
            
            Grading:
            - Homework: 30%
            - Midterm Exam: 30%
            - Final Exam: 40%
            
            Textbook: "Introduction to Algorithms" by Cormen, Leiserson, Rivest, and Stein
            """
        },
        {
            "title": "CSCE 636 - Deep Learning",
            "content": """
            CSCE 636 - Deep Learning (3 credit hours)
            
            Prerequisites: CSCE 633 (Machine Learning) or equivalent, Linear Algebra, Calculus
            
            Course Description:
            Introduction to deep learning methods and applications. Topics include neural networks,
            convolutional neural networks, recurrent neural networks, autoencoders, generative
            adversarial networks, and transformer architectures.
            
            Learning Objectives:
            - Understand fundamental concepts of deep learning
            - Implement neural networks from scratch
            - Apply deep learning to computer vision and NLP tasks
            - Use popular deep learning frameworks (PyTorch, TensorFlow)
            
            Projects:
            - Image classification using CNNs
            - Sentiment analysis with RNNs
            - Final project on chosen topic
            
            Grading:
            - Projects: 50%
            - Midterm: 20%
            - Final: 30%
            """
        },
        {
            "title": "ECEN 649 - Pattern Recognition",
            "content": """
            ECEN 649 - Pattern Recognition (3 credit hours)
            
            Prerequisites: ECEN 601 (Linear System Theory) and knowledge of probability theory
            
            Course Description:
            Statistical and structural approaches to pattern recognition. Topics include 
            Bayesian decision theory, parametric and non-parametric classification methods,
            feature selection and extraction, clustering algorithms, and neural networks.
            
            Learning Objectives:
            - Understand statistical pattern recognition theory
            - Implement classification and clustering algorithms
            - Apply pattern recognition to real-world problems
            - Evaluate classifier performance
            
            Laboratory Component:
            Hands-on implementation of pattern recognition algorithms using MATLAB and Python
            
            Grading:
            - Homework: 25%
            - Lab Reports: 25%
            - Midterm: 25%
            - Final Project: 25%
            """
        },
        {
            "title": "MS Degree Requirements - CSCE",
            "content": """
            Master of Science in Computer Science and Engineering
            
            Degree Requirements:
            
            Thesis Option (32 credit hours):
            - Core courses: 12 credit hours
            - Elective courses: 14 credit hours  
            - Thesis: 6 credit hours (CSCE 691)
            
            Non-Thesis Option (36 credit hours):
            - Core courses: 12 credit hours
            - Elective courses: 21 credit hours
            - Project: 3 credit hours (CSCE 689)
            
            Core Course Requirements:
            Students must take courses from at least 3 of the following areas:
            1. Algorithms and Theory
            2. Computer Systems
            3. Software Engineering
            4. Artificial Intelligence/Machine Learning
            5. Computer Graphics/Visualization
            6. Computer Networks
            
            Research Areas:
            - Artificial Intelligence and Machine Learning
            - Computer Systems and Architecture
            - Cybersecurity
            - Data Science and Analytics
            - Human-Computer Interaction
            - Software Engineering
            
            Admission Requirements:
            - Bachelor's degree in Computer Science or related field
            - GPA: 3.0 or higher
            - GRE scores (recommended)
            - Letters of recommendation
            """
        },
        {
            "title": "PhD Degree Requirements - ECEN",
            "content": """
            Doctor of Philosophy in Electrical and Computer Engineering
            
            Degree Requirements:
            
            Minimum 96 credit hours beyond bachelor's degree, including:
            - Coursework: 64 credit hours minimum
            - Dissertation: 32 credit hours (ECEN 691)
            
            Coursework Distribution:
            - Major area: 24 credit hours minimum
            - Minor area: 12 credit hours minimum  
            - Supporting courses: 28 credit hours minimum
            
            Major Areas of Study:
            1. Communications, Networks, and Signal Processing
            2. Computer Engineering
            3. Electromagnetics and Microwaves
            4. Electronic Devices and Materials
            5. Power and Energy Systems
            6. Control Systems
            
            Qualifying Examination:
            - Written exam in major area
            - Must be passed within 3 attempts
            - Typically taken after 2 years of study
            
            Preliminary Examination:
            - Oral defense of dissertation proposal
            - Formation of dissertation committee
            - Must be completed before final year
            
            Final Examination:
            - Oral defense of completed dissertation
            - Open to university community
            
            Residency Requirement:
            - Minimum 2 consecutive semesters in residence
            - Full-time enrollment required
            """
        }
    ]
    
    return sample_courses

def create_sample_pdfs():
    """Create sample PDF files for testing"""
    
    # Create Database directory
    if not os.path.exists("Database"):
        os.makedirs("Database")
        print("✅ Created Database/ directory")
    
    sample_courses = create_sample_pdf_content()
    
    for i, course in enumerate(sample_courses):
        filename = f"Database/course_{i+1}_{course['title'].replace(' ', '_').replace('-', '').replace('/', '_')}.pdf"
        
        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph(course['title'], styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Content
        content_paragraphs = course['content'].strip().split('\n\n')
        for para in content_paragraphs:
            if para.strip():
                p = Paragraph(para.strip(), styles['Normal'])
                story.append(p)
                story.append(Spacer(1, 6))
        
        doc.build(story)
        print(f"✅ Created {filename}")
    
    print(f"\n🎉 Successfully created {len(sample_courses)} sample PDF files!")
    return len(sample_courses)

def create_simple_text_files():
    """Alternative: Create simple text files if PDF creation fails"""
    
    if not os.path.exists("Database"):
        os.makedirs("Database")
        print("✅ Created Database/ directory")
    
    sample_courses = create_sample_pdf_content()
    
    for i, course in enumerate(sample_courses):
        filename = f"Database/course_{i+1}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(course['title'] + '\n\n')
            f.write(course['content'])
        
        print(f"✅ Created {filename}")
    
    print(f"\n🎉 Successfully created {len(sample_courses)} sample text files!")
    return len(sample_courses)

def main():
    """Main function to create sample data"""
    print("🚀 Creating sample academic data for testing...")
    print("-" * 50)
    
    try:
        # Try to create PDFs first
        count = create_sample_pdfs()
        print(f"\n📚 Created {count} sample PDF files in Database/ folder")
        print("📝 These files contain sample course information for CSCE and ECEN departments")
        
    except ImportError:
        print("⚠️  reportlab not installed. Creating text files instead...")
        print("💡 To create PDFs, install reportlab: pip install reportlab")
        count = create_simple_text_files()
        print(f"\n📚 Created {count} sample text files in Database/ folder")
    
    except Exception as e:
        print(f"❌ Error creating PDFs: {e}")
        print("📄 Creating text files as fallback...")
        count = create_simple_text_files()
        print(f"\n📚 Created {count} sample text files in Database/ folder")
    
    print("\n🎯 Next steps:")
    print("1. Create your Pinecone index named 'indianconsti'")
    print("2. Run: python generate_embeddings.py")
    print("3. Run: python app.py")
    print("4. Test the chatbot with questions like:")
    print("   - 'What are the requirements for MS in Computer Science?'")
    print("   - 'Tell me about CSCE 629'")
    print("   - 'What are the PhD requirements for ECEN?'")

if __name__ == "__main__":
    main()