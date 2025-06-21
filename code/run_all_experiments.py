#!/usr/bin/env python3
"""
run_all_experiments.py
Execute complete AGI impossibility proof suite
"""

import subprocess
import time
import os
import json

def check_api_keys():
    """Verify API keys are set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ Missing ANTHROPIC_API_KEY in .env file")
        return False
    
    print("✅ API key found")
    return True

def run_all():
    """Execute all experiments"""
    print("🚀 AGI IMPOSSIBILITY PROOF SUITE")
    print("=" * 60)
    print("Using Claude API to prove AGI is impossible")
    print("=" * 60)
    
    if not check_api_keys():
        print("\n⚠️  Please add your ANTHROPIC_API_KEY to .env file")
        return
    
    experiments = [
        'pattern_overflow_api.py',
        'cascade_corruption_api.py', 
        'human_filter_api.py'
    ]
    
    results = []
    
    for i, script in enumerate(experiments, 1):
        print(f"\n\n{'='*60}")
        print(f"Experiment {i}/3: {script}")
        print(f"{'='*60}")
        
        try:
            subprocess.run(['python', script], check=True)
            results.append(f"✅ {script}")
        except:
            results.append(f"❌ {script}")
        
        if i < len(experiments):
            print("\n⏳ Pausing before next experiment...")
            time.sleep(3)
    
    print("\n\n" + "="*60)
    print("COMPLETE RESULTS")
    print("="*60)
    
    for result in results:
        print(result)
    
    # Generate summary
    generate_summary()

def generate_summary():
    """Create a master summary of all results"""
    summary = {
        'title': 'AGI Impossibility: Experimental Proof',
        'experiments': {}
    }
    
    # Load all result files
    result_files = [
        'pattern_overflow_results.json',
        'cascade_corruption_results.json',
        'human_filter_results.json'
    ]
    
    for file in result_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                data = json.load(f)
                experiment_name = file.replace('_results.json', '')
                summary['experiments'][experiment_name] = data.get('summary', {})
    
    with open('agi_impossibility_proof.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n📊 Master summary saved to: agi_impossibility_proof.json")
    print("\n🎯 Ready to publish with reproducible experiments!")

if __name__ == "__main__":
    run_all()