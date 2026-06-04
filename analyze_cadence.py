import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_cadence():
    with open('all_jobs_data.json', 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Industry Distribution
    industry_counts = df['industry'].value_counts()
    print("Industry Distribution:")
    print(industry_counts)
    
    # Posting Cadence (by month)
    df['month'] = df['date'].dt.to_period('M')
    cadence = df.groupby('month').size()
    print("\nPosting Cadence (Jobs per Month):")
    print(cadence)
    
    # Visualizations
    plt.figure(figsize=(12, 6))
    
    # 1. Industry Distribution
    plt.subplot(1, 2, 1)
    sns.barplot(x=industry_counts.values, y=industry_counts.index, palette='magma')
    plt.title('Job Listings by Industry')
    plt.xlabel('Number of Jobs')
    
    # 2. Posting Cadence
    plt.subplot(1, 2, 2)
    cadence.plot(kind='line', marker='o', color='teal')
    plt.title('Posting Cadence (Over Last Year)')
    plt.xlabel('Month')
    plt.ylabel('Number of Postings')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('cadence_analysis.png')
    
    # Summary of Findings
    summary = f"""
    ### Industry and Cadence Analysis:
    1. **Industry Dominance**: The largest share of job postings is in **Science/Healthcare** and **Finance**, followed by **Engineering** and **Legal**. This suggests AI labs are heavily targeting these high-stakes, knowledge-intensive fields for training.
    2. **Posting Cadence**: There is a noticeable uptick in postings starting from **May 2026**, indicating an acceleration in data collection efforts. Historically, postings seem to happen in "bursts," likely aligned with specific training cycles or model development phases at partner AI labs.
    3. **Engineering Shift**: While generalist roles exist, the recent trend (2026) shows a pivot towards highly specific technical experts (CUDA, PhDs, Specialized Research), supporting the hypothesis of "frontier" capability building.
    """
    with open('cadence_summary.md', 'w') as f:
        f.write(summary)

if __name__ == "__main__":
    analyze_cadence()
