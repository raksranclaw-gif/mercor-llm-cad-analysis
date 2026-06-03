import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

def parse_pay(pay_str):
    # Extract numbers from strings like "$30-$60 / hr"
    nums = re.findall(r'\d+', pay_str)
    if not nums:
        return 0
    nums = [int(n) for n in nums]
    return sum(nums) / len(nums)

def analyze_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    df['avg_pay'] = df['pay_range'].apply(parse_pay)
    
    # Analysis 1: Pay vs Expertise
    print("Average Pay by Role Type:")
    print(df[['title', 'avg_pay']])
    
    # Analysis 2: Task Nature
    print("\nCommon Task Types:")
    all_tasks = [task for sublist in df['tasks'].tolist() for task in sublist]
    for task in set(all_tasks):
        print(f"- {task}")

    # Visualization: Pay Distribution
    plt.figure(figsize=(10, 6))
    sns.barplot(x='avg_pay', y='title', data=df.sort_values('avg_pay', ascending=False), palette='viridis')
    plt.title('Average Hourly Pay for AI Training Roles on Mercor')
    plt.xlabel('Average Hourly Pay ($)')
    plt.ylabel('Job Title')
    plt.tight_layout()
    plt.savefig('pay_analysis.png')
    
    # Summary of findings
    summary = """
    ### Findings Summary:
    1. **Knowledge Intensive Work**: Jobs explicitly require expertise in CAD (AutoCAD, SolidWorks), Engineering (PhD level), and professional software.
    2. **Low Relative Pay**: While $30-$100/hr sounds high for gig work, it is often significantly lower than the market rate for specialized PhD-level engineers or CAD experts in full-time roles, especially considering the lack of benefits and the "pittance" nature for the value provided to frontier AI labs.
    3. **Direct Link to LLM Capabilities**: Job descriptions explicitly mention "improving how AI systems understand complex software interfaces," "advancing engineering problem-solving," and "training frontier models."
    4. **Workflow Capture**: The requirement to "record screen sessions" and "annotate screenshots" suggests that LLMs are being trained on actual human expert workflows in professional software, directly explaining recent jumps in CAD and engineering reasoning capabilities.
    """
    with open('summary.md', 'w') as f:
        f.write(summary)

if __name__ == "__main__":
    analyze_data()
