import json
import requests


class GitLabHandler:

    def __init__(self, config={}, rootURI="", PAT="", projectID="", user=""):
        if config:
            self.rootURI = config["rootURI"]
            self.PAT = config["PAT"]
            self.projectID = config["projectID"]
            self.user = config["user"]
        else:
            self.rootURI = rootURI
            self.PAT = PAT
            self.projectID = projectID
            self.user = user

    def get_all_issues(self):
        return self._get(f"projects/{self.projectID}/issues")

    def get_my_issues(self):
        return self._get(f"projects/{self.projectID}/issues",
                         {"assignee_username": self.user})

    def get_issue(self, id):
        return self._get(f"projects/{self.projectID}/issues/{id}")

    def update_estimate(self, id, value):
        return self._post(f"projects/{self.projectID}/issues/{id}/time_estimate",
                          {"duration": value})

    def update_spent(self, id, value):
        return self._post(f"projects/{self.projectID}/issues/{id}/add_spent_time",
                          {"duration": value})

    def reset_estimate(self, id):
        return self._post(f"projects/{self.projectID}/issues/{id}/reset_time_estimate")

    def reset_spent(self, id):
        return self._post(f"projects/{self.projectID}/issues/{id}/reset_spent_time")

    def set_sprint(self, issue_id, sprint_no):
        sprint_id = 0 # Default to ID of 0
        # Check if sprint_no is valid
        if (sprint_no != "0"):
            milestone_data = self._get(f"projects/{self.projectID}/milestones/")
            sprint_id = self._find_milestone_id(sprint_no, milestone_data)
            # Check if not found
            if (sprint_id == -1):
                return "No Change made"

        return self._put(f"projects/{self.projectID}/issues/{issue_id}",
                         {"milestone_id": sprint_id})

    def _get(self, uriEnd, params={}):
        res = requests.get(f"{self.rootURI}{uriEnd}",
                           headers={"PRIVATE-TOKEN": self.PAT},
                           params=params)

        if (res.status_code == 200):
            return self._dictify(res.content)
        else:
            return res.status_code

    def _post(self, uriEnd, params={}):
        res = requests.post(f"{self.rootURI}{uriEnd}",
                            headers={"PRIVATE-TOKEN": self.PAT},
                            params=params)

        if (res.status_code == 200):
            return self._dictify(res.content)
        else:
            return res.status_code

    def _put(self, uriEnd, params={}):
        res = requests.put(f"{self.rootURI}{uriEnd}",
                           headers={"PRIVATE-TOKEN": self.PAT},
                           params=params)

        if (res.status_code == 200):
            return self._dictify(res.content)
        else:
            return res.status_code

    def _dictify(self, data):
        json_string = data.decode("ascii")
        return json.loads(json_string)

    def _find_milestone_id(self, sprint_no, milestone_data):
        """ Find the milestone ID for the sprint with the specified number (Otherwise -1) """
        for entry in milestone_data:
            if entry["title"] == f"Sprint {sprint_no}":
                return entry["id"]

        return -1
