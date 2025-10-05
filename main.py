import os
import json
from core.task_manager import TaskManager

def main(fresh_start):
    project_name = "A chat app use modern lay-out with dark theme creat by use Nextjs"

    print(f"\n=== Starting Project: {project_name} === (fresh_start={fresh_start})\n")

    # Initialize TaskManager and run project
    tm = TaskManager()
    result = tm.run_project(project_name, fresh_start=fresh_start)

    # Print all subtask results
    print("\n=== Subtask Results ===\n")
    for idx, sub in enumerate(result["results"], 1):
        print(f"Subtask {idx}: {sub.get('subtask')}")
        print(f"Status: {sub.get('status')}")
        if sub.get("result"):
            print("Developer Output:")
            print(sub.get("result"))
        if sub.get("review"):
            print("Review Output:")
            print(sub.get("review"))
        if sub.get("discussion"):
            print("Discussion Notes:")
            print(sub.get("discussion"))
        if sub.get("error"):
            print("Error:", sub.get("error"))
        print("-" * 50)

    # Print project summary
    print("\n=== Project Summary ===")
    print(result.get("summary"))

    # Show final context JSON path
    report_path = result.get("report")
    print(f"\n=== Project Context JSON Path ===\n{report_path}")

    # Load and inspect saved context JSON
    if os.path.exists(report_path):
        print("\n=== Saved Context Contents ===")
        with open(report_path, "r", encoding="utf-8") as f:
            context_data = json.load(f)
            for st in context_data.get("subtasks", []):
                dev_short = st['developer_output'][:100].replace("\n", " ")
                rev_short = st['review_output'][:100].replace("\n", " ")
                disc_short = st['discussion'][:100].replace("\n", " ")
                print(f"{st['timestamp']} | Subtask: {st['subtask']} | Status: {st['status']}")
                print(f"  Developer: {dev_short}...")
                print(f"  Review: {rev_short}...")
                print(f"  Discussion: {disc_short}...")
                print("-" * 50)

if __name__ == "__main__":
    # Run fresh start test
    main(fresh_start=True)

