# Gitlab Time Tracker

## Configuration
Move `template.config.yaml` to `config.yaml` and add the corresponding values required.

## Usage
To Launch run:
```
python3 time.py -i
```
or
```
python3 time.py [OPTIONS]
```

By default easiest method is using interactive mode `-i` otherwise commands can be manually specified using the options below.

### Options

Options for displaying issues:

| Option | Usage |
|--------|-------|
| --show-all, -a | Show all of the issues in your projects |
| --show-mine, -m | Show the issues that are assigned to you in your projects |
| --show ID, -s ID | Show detailed information about the issue with the specified ID (Including description, time spent, estimated time) |
| --filter, -f | Filter the tickets based on their status (opened or closed) |

Options for updating issues: Requires the use of ID tag to determine which issue to update.

| Option | Usage |
|--------|-------|
| --issue-id ID, -id ID | Specify the issue ID number for use with estimates/spent time |
| --estimate TIME_STR, -e TIME_STR | Set the estimated time for an issue (Relys on iid) |
| --spend TIME_STR | Add to the spent time for an issue (Relys on iid) |
