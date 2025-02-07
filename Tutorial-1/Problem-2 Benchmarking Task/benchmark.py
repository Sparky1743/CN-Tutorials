import subprocess
import time

def run_benchmark(num_clients):
    command = f"bash start.sh client_side2.py {num_clients}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    # Extract execution time from output
    for line in output.decode().split('\n'):
        if "Total Execution Time:" in line:
            return float(line.split(":")[1].strip().split()[0])
    return None

client_counts = list(range(10, 101, 10))
execution_times = []

for count in client_counts:
    print(f"Running benchmark with {count} clients...")
    execution_time = run_benchmark(count)
    if execution_time:
        execution_times.append(execution_time)
    else:
        print(f"Error running benchmark for {count} clients")
    time.sleep(2)  # Wait between runs to allow server to reset

print("\nResults:")
print("Clients | Execution Time (s)")
print("--------|--------------------")
for count, time in zip(client_counts, execution_times):
    print(f"{count:7d} | {time:.6f}")

# We can now use client_counts and execution_times lists for further analysis or plotting
print(execution_times)
print(client_counts)
