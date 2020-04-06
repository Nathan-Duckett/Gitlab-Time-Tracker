import argparse
import yaml

from gitlabhandler import GitLabHandler

# Must be before data declaration
def load_config():
    """Load yaml config"""
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        return config

# Data handler declaration in global scope
data = GitLabHandler(config=load_config())

def print_help():
    print("Available commands:")
    print("show all - Shows all issues in the repo")
    print("show mine - Shows all issues assigned to your user")
    print("show sprint :id - Shows all issues relating to the specified sprint number")
    print("show :id - Shows information about a specific issue")
    print("spend :id :timestr - Spends the timestr amount of time on the specific issue")
    print("estimate :id :timestr - Sets the estimated time of the issue to the value of timestr")
    print("reset estimate :id - resets the estimated time")
    print("reset spent :id - resets the time spent on the issue")
    print("set sprint :id :sprint_number - Sets the issue into the milestone matching the sprint number")
    print("---")
    print("timestr is a human readable format of time using (S, M, H, D, M)")
    print("Can be combined e.g. 1h30m or 2d4h to set the estimated or spent time")
    print("-------------\n")


def process_input(value):
    if (value == "show all"):
        show_all()
    elif (value == "show mine"):
        show_mine()
    elif (value.startswith("show sprint ")):
        id = extract_id(value, 2)
        show_sprint(id)
    elif (value.startswith("show ")):
        id = extract_id(value)
        show_specific(id)
    elif (value.startswith("spend ")):
        id = extract_id(value)
        time_str = extract_time(value)
        spend(id, time_str)
    elif (value.startswith("estimate ")):
        id = extract_id(value)
        time_str = extract_time(value)
        estimate(id, time_str)
    elif (value.startswith("reset estimate ")):
        id = extract_id(value, 2)
        reset_estimate(id)
    elif (value.startswith("reset spent ")):
        id = extract_id(value, 2)
        reset_spend(id)
    elif (value.startswith("set sprint ")):
        id = extract_id(value, 2)
        sprint_no = extract_id(value, 3)
        set_sprint(id, sprint_no)
    else:
        print("Invalid option - Please try again")


def extract_id(value, indent=1):
    content = value.split(" ")
    return content[indent]

def extract_time(value, indent=2):
    content = value.split(" ")
    return content[indent]

def show_all(filter=None):
    out = data.get_all_issues()
    print_issue_list(out, filter)

def show_specific(id):
    out = data.get_issue(id)
    fstr = f"{out['iid']} | {out['state']} | {out['title']}"
    print(fstr)
    print(f"Description: {out['description']}")
    print(f"Time Spent: {out['time_stats']['human_total_time_spent']}  Estimated Time: {out['time_stats']['human_time_estimate']}")


def show_mine(filter=None):
    out = data.get_my_issues()
    print_issue_list(out, filter)


def show_sprint(sprint_number, filter=None):
    out = data.get_sprint_issues(f"Sprint {sprint_number}")
    print_issue_list(out, filter)


def print_issue_list(out, filter):
    for entry in out:
        # Add filter on issue state
        if filter != None:
            if entry['state'] != filter:
                continue
        
        fstr = f"{entry['iid']} | {entry['state']} | {entry['title']}"
        print(fstr)
    
    # Output final empty line
    print("\n")
    return

def spend(id, time_str):
    out = data.update_spent(id, time_str)
    if (out == 201):
        print(f"Successfully spent {time_str} on ticket {id}")
    return


def reset_spend(id):
    out = data.reset_spent(id)
    if out['total_time_spent'] == 0:
        print(f"Successfully reset time spent to 0 on ticket {id}")
    return


def estimate(id, time_str):
    out = data.update_estimate(id, time_str)
    if out['human_time_estimate'] == time_str:
        print(f"Successfully updated time estimate to {time_str} on ticket {id}")
    return


def reset_estimate(id):
    out = data.reset_estimate(id)
    if out['total_time_estimate'] == 0:
        print(f"Successfully reset time estimate to 0 on ticket {id}")
    return

def set_sprint(id, sprint_no):
    out = data.set_sprint(id, sprint_no)
    if out == "No Change made":
        print(out)
    elif isinstance(out, int):
        print(out)
    else:
        print(f"Sucessfully set issue {id} to Sprint {sprint_no}")
    return


def main():
    parser = argparse.ArgumentParser()
    # Interactive Mode
    parser.add_argument("--interactive", "-i", help="Interactive version of the application", action="store_true")

    # Complete modes
    parser.add_argument("--show-all", "-a", help="Show all issues", action="store_true")
    parser.add_argument("--show-mine", "-m", help="Show my issues", action="store_true")
    parser.add_argument("--show-sprint", "-sprint", help="Show issues relating to the specified sprint number")
    parser.add_argument("--show", "-s", help="Show an issue - Based on id")
    parser.add_argument("--filter", "-f", help="Filter the shown issues with a specific value")

    parser.add_argument("--issue-id", "-id", help="Specify the issue ID number for use with estimates/spent time") 
    parser.add_argument("--estimate", "-e", help="Set the estimated time for an issue (Relys on iid)") 
    parser.add_argument("--spend", help="Add to the spent time for an issue (Relys on iid)")
    parser.add_argument("--set-sprint", help="Set the Sprint Number on this Issue (Relys on iid)")

    args = parser.parse_args()

    if (args.interactive):
        running = True
        while(running):
            value = input("Choose what you want to do (h for help): ")

            if value == "q":
                exit(0)
            elif value == "h":
                print_help()
            else:
                process_input(value)
    elif args.show_all:
        show_all(filter=args.filter)
    elif args.show_mine:
        show_mine(filter=args.filter)
    elif args.show_sprint:
        show_sprint(args.show_sprint, filter=args.filter)
    elif args.show:
        show_specific(args.show)
    elif args.issue_id:
        if args.estimate:
            estimate(args.issue_id, args.estimate)
        elif args.spend:
            spend(args.issue_id, args.spend)
        elif args.set_sprint:
            set_sprint(args.issue_id, args.set_sprint)
        else:
            print("No option chosen to handle ticket ID")
    else:
        print("You must provide arguments to run this script: If unsure use -i")


if __name__ == '__main__':
    main()