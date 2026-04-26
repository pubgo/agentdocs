#!/usr/bin/env python3
"""Analyze coagent session events from stdin and output a Mermaid diagram."""

import json
import sys


def main():
    data = json.load(sys.stdin)
    if not isinstance(data, list):
        print("Error: expected a JSON array of events", file=sys.stderr)
        sys.exit(1)

    turns = []
    subagents = []
    tool_calls = []
    other = 0

    for evt in data:
        t = evt.get("type", "")
        if "_delta" in t:
            continue
        if t == "assistant.turn_start":
            turns.append(evt)
        elif t == "subagent.started":
            subagents.append(evt)
        elif t == "tool.execution_start":
            tool_calls.append(evt)
        else:
            other += 1

    # Summary
    print("## Summary\n")
    print(f"- **Turns**: {len(turns)}")
    print(f"- **Subagents**: {len(subagents)}")
    print(f"- **Tool calls**: {len(tool_calls)}")
    print(f"- **Total events** (excl. deltas): {len([e for e in data if '_delta' not in e.get('type', '')])}")
    print()

    # Build Mermaid
    print("## Mermaid Diagram\n")
    print("```mermaid")
    print("graph TD")

    node_id = 0
    turn_nodes = {}
    tc_nodes = {}

    # Turns
    for evt in data:
        t = evt.get("type", "")
        d = evt.get("data", {})
        if "_delta" in t:
            continue

        if t == "assistant.turn_start":
            turn_id = d.get("turnId", f"turn_{node_id}")
            nid = f"T{node_id}"
            node_id += 1
            label = f"Turn {turn_id}"
            turn_nodes[turn_id] = nid
            print(f'    {nid}["{_esc(label)}"]')

        elif t == "subagent.started":
            name = d.get("name", "subagent")
            parent_tc = d.get("parentToolCallId", "")
            nid = f"S{node_id}"
            node_id += 1
            print(f'    {nid}[/"{_esc(name)}"/]')
            if parent_tc and parent_tc in tc_nodes:
                print(f"    {tc_nodes[parent_tc]} --> {nid}")

        elif t == "tool.execution_start":
            tc_id = d.get("toolCallId", f"tc_{node_id}")
            tool_name = d.get("name", d.get("toolName", "tool"))
            parent_tc = d.get("parentToolCallId", "")
            turn_id = d.get("turnId", "")
            nid = f"C{node_id}"
            node_id += 1
            tc_nodes[tc_id] = nid
            print(f'    {nid}("{_esc(tool_name)}")')

            if parent_tc and parent_tc in tc_nodes:
                print(f"    {tc_nodes[parent_tc]} --> {nid}")
            elif turn_id and turn_id in turn_nodes:
                print(f"    {turn_nodes[turn_id]} --> {nid}")

    print("```")


def _esc(s):
    """Escape characters that break Mermaid labels."""
    return str(s).replace('"', "'").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    main()
