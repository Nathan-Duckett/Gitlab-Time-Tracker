# Gitlab Time Tracker

## Configuration
Move `template.config.yaml` to `config.yaml` and add the corresponding values required.
```yaml
rootURI: 'gitlab api endpoint e.g. "https://gitlab.ecs.vuw.ac.nz/api/v4/"'
PAT: 'Personal Access Token generated from gitlab'
user: 'Your gitlab user name to match tickets to'
projectID: 'Project ID of the repo you want to manage'
```
You must [Generate PAT](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) for your profile with **API** privileges.

If you do not already have both `pyyaml` and `requests` python libraries installed use to install all dependencies:
```bash
python3 -m pip install -r requirements.txt
``` 

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
| --show-mine, -f | Show the issues that are assigned to you in your projects |
| --show ID, -s ID | Show detailed information about the issue with the specified ID (Including description, time spent, estimated time) |

Options for updating issues: Requires the use of ID tag to determine which issue to update.

| Option | Usage |
|--------|-------|
| --issue-id ID, -id ID | Specify the issue ID number for use with estimates/spent time |
| --estimate TIME_STR, -e TIME_STR | Set the estimated time for an issue (Relys on iid) |
| --spend TIME_STR | Add to the spent time for an issue (Relys on iid) |
| --set-sprint SPRINT_NO | Set the issue to be part of the sprint number provided (Relys on iid) |