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

```bash
usage: time.py [-h] [--interactive] [--show-all] [--show-mine]
               [--show-sprint SHOW_SPRINT] [--show SHOW] [--filter FILTER]
               [--issue-id ISSUE_ID] [--estimate ESTIMATE] [--spend SPEND]
               [--set-sprint SET_SPRINT]
               [--issue-ids ISSUE_IDS [ISSUE_IDS ...]]

optional arguments:
  -h, --help            show this help message and exit
  --interactive, -i     Interactive version of the application
  --show-all, -a        Show all issues
  --show-mine, -m       Show my issues
  --show-sprint SHOW_SPRINT, -ss SHOW_SPRINT
                        Show issues relating to the specified sprint number
  --show SHOW, -s SHOW  Show an issue - Based on id
  --filter FILTER, -f FILTER
                        Filter the shown issues with a specific value
  --issue-id ISSUE_ID, -id ISSUE_ID
                        Specify the issue ID number for use with
                        estimates/spent time
  --estimate ESTIMATE, -e ESTIMATE
                        Set the estimated time for an issue (Relys on iid)
  --spend SPEND         Add to the spent time for an issue (Relys on iid)
  --set-sprint SET_SPRINT, -sprint SET_SPRINT
                        Set the Sprint Number on this Issue (Relys on iid)
  --issue-ids ISSUE_IDS [ISSUE_IDS ...], -ids ISSUE_IDS [ISSUE_IDS ...]
                        Specifiy multiple issue ids to bulk assign to a sprint
```