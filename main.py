#!/usr/bin/env python3

import sys
import os
import argparse
import json

from datetime import datetime
from collections import defaultdict


def parse_args(args):
    parser = argparse.ArgumentParser(description="This script converts tasks exported from Remember The Milk app "
                                                 "to Singularity importable CSV file")
    parser.add_argument('--source',
                        help='Path to source file (e.g. rememberthemilk_export_2022-06-20T15_07_39.322Z.json)',
                        required=True)
    parser.add_argument('--output',
                        help='Where to save results', default='output.csv',
                        required=False)
    parser.add_argument('--preserve-completed', action='store_true', dest='preserve_completed',
                        help='Convert and save info about completed tasks to output file.',
                        required=False)

    return parser.parse_args(args)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    params = parse_args(args)

    if not os.path.exists(params.source):
        print(f'ERROR: File not found {params.source}')
        return 1

    with open(params.source) as f:
        input_data = json.loads(f.read())

    lists = {}

    for list_id, list_name in [(l['id'], l['name']) for l in input_data['lists']]:
        lists[list_id] = {
            'name': list_name,
            'tasks': [],
        }
    print(f'Loaded {len(lists)} Lists')

    notes = defaultdict(lambda: [])

    for series_id, text in [(l['series_id'], l['content']) for l in input_data['notes']]:
        notes[series_id].append(text)
    print(f'Loaded {len(notes)} Note series')

    tasks = {}
    subtasks = defaultdict(lambda: [])

    for task_data in input_data['tasks']:
        extra_data = []

        if 'date_trashed' in task_data:
            continue

        if 'url' in task_data:
            extra_data.append(f'URL: {task_data["url"]}')

        if len(task_data['tags']) > 0:
            extra_data.append(f'Tags: {", ".join(task_data["tags"])}')

        if 'repeat' in task_data:
            extra_data.append(f'Repeat info: {task_data["repeat"]}')

        if 'date_due' in task_data:
            due_date = datetime.fromtimestamp(task_data['date_due']/1000).isoformat()
            if not task_data['date_due_has_time']:
                due_date = due_date[:-9]
        else:
            due_date = ''

        status = '+' if 'date_completed' in task_data else ''
        if status == '+' and not params.preserve_completed:
            continue

        task = {
            'id': task_data['id'],
            'name': task_data['name'].replace('"', "'"),
            'description_lines': extra_data + notes[task_data['series_id']],
            'status': status,
            'due_date': due_date,
            'subtasks': [],
        }

        if 'parent_id' in task_data:
            subtasks[task_data['parent_id']].append(task)
        else:
            tasks[task_data['id']] = task

        lists[task_data['list_id']]['tasks'].append(task)

    print(f'Loaded {len(tasks)} tasks')

    output_lines = [
        'Id,Type,Name,Description,Priority,Status,Date,Deadline\n',
        '1,Project,Remember The Milk,,,,,\n',
    ]

    for list_index, list_data in enumerate(lists.values(), start=1):
        output_lines.append(f'1.{list_index},Project,{list_data["name"]},,,,,\n')
        for task_index, task_data in enumerate(list_data['tasks'], start=1):
            description = '\n'.join([line.replace('"', "'") for line in task_data['description_lines']])
            output_lines.append(f'1.{list_index}.{task_index},'
                                f'Task,'
                                f'"{task_data["name"]}",'
                                f'"{description}",'
                                f','
                                f'{task_data["status"]},'
                                f'{task_data["due_date"]},'
                                f'\n')
            for subtask_index, subtask_data in enumerate(subtasks[task_data['id']], start=1):
                description = '\n'.join([line.replace('"', "'") for line in subtask_data['description_lines']])
                output_lines.append(f'1.{list_index}.{task_index}.{subtask_index},'
                                    f'Task,'
                                    f'"{subtask_data["name"]}",'
                                    f'"{description}",'
                                    f','
                                    f'{subtask_data["status"]},'
                                    f'{subtask_data["due_date"]},'
                                    f'\n')

    with open(params.output, 'w') as f:
        f.writelines(output_lines)

    return 0


if __name__ == '__main__':
    sys.exit(main())
