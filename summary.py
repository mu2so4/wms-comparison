import os
import csv
import statistics
from pathlib import Path
import matplotlib.pyplot as plt

def parse_benchmark_file(path):
    with open(path) as f:
        lines = f.read().strip().splitlines()
    wms = lines[0].strip()
    container = lines[1].strip()
    times = [float(line) for line in lines[2:]]
    return wms, container, times

def read_all_benchmarks(results_dir):
    benchmarks = []
    for filename in os.listdir(results_dir):
        filepath = os.path.join(results_dir, filename)
        wms, container, times = parse_benchmark_file(filepath)
        avg = statistics.mean(times)
        stdev = statistics.stdev(times) if len(times) > 1 else 0.0
        benchmarks.append({
            'filename': filename,
            'wms': wms,
            'container': container,
            'times': times,
            'avg': avg,
            'stdev': stdev,
        })
    return benchmarks

def find_reference_case(benchmarks):
    for b in benchmarks:
        if b['wms'] == 'Native' and b['container'] == 'Local':
            return b['avg']
    raise ValueError("Reference case (Native + Local) not found.")

def compute_overheads(benchmarks, reference_avg):
    for b in benchmarks:
        b['overhead'] = b['avg'] / reference_avg if b['avg'] > 0 else float('inf')

def sort_key(b):
    return (
        0 if b['wms'] == 'Native' else 1, b['wms'],
        0 if b['container'] == 'Local' else 1, b['container']
    )

def save_to_csv(benchmarks, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['WMS', 'Container', 'AvgTime', 'StdDev', 'Overhead'])
        for b in benchmarks:
            writer.writerow([b['wms'], b['container'], f"{b['avg']:.4f}", f"{b['stdev']:.4f}", f"{b['overhead']:.4f}"])

def save_graphs(benchmarks, output_dir):
    # Bar chart of average time
    labels = [f"{b['wms']}\n{b['container']}" for b in benchmarks]
    avg_times = [b['avg'] for b in benchmarks]
    stdevs = [b['stdev'] for b in benchmarks]

    plt.figure(figsize=(12, 6))
    plt.bar(labels, avg_times, yerr=stdevs, capsize=5)
    plt.ylabel('Average Time (s)')
    plt.title('Benchmark Average Times with StdDev')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_dir / 'avg_times.png')
    plt.close()

    # Bar chart of overheads
    overheads = [b['overhead'] for b in benchmarks]

    plt.figure(figsize=(12, 6))
    plt.bar(labels, overheads, color='green')
    plt.ylabel('Overhead (relative to Native+Local)')
    plt.title('Benchmark Overheads')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_dir / 'overheads.png')
    plt.close()

def main():
    results_dir = 'results'
    summary_dir = Path('summary')
    summary_dir.mkdir(exist_ok=True)
    output_file = summary_dir / 'summary.csv'

    benchmarks = read_all_benchmarks(results_dir)
    reference_avg = find_reference_case(benchmarks)
    compute_overheads(benchmarks, reference_avg)
    benchmarks.sort(key=sort_key)
    save_to_csv(benchmarks, output_file)
    save_graphs(benchmarks, summary_dir)

if __name__ == '__main__':
    main()

