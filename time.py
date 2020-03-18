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
    print("show :id - Shows information about a specific issue")
    print("spend :id :timestr - Spends the timestr amount of time on the specific issue")
    print("estimate :id :timestr - Sets the estimated time of the issue to the value of timestr")
    print("reset estimate :id - resets the estimated time")
    print("reset spent :id - resets the time spent on the issue")
    print("---")
    print("timestr is a human readable format of time using (S, M, H, D, M)")
    print("Can be combined e.g. 1h30m or 2d4h to set the estimated or spent time")
    print("-------------\n")


def process_input(value):
    if (value == "show all"):
        show_all()
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
    else:
        print("Invalid option - Please try again")


def extract_id(value, indent=1):
    content = value.split(" ")
    return content[indent]

def extract_time(value, indent=2):
    content = value.split(" ")
    return content[indent]

def show_all():
    out = data.get_all_issues()

    for entry in out:
        # print(entry)
        fstr = f"{entry['iid']} | {entry['state']} | {entry['title']}"
        print(fstr)

    # Output final empty line
    print("\n")

def show_specific(id):
    out = data.get_issue(id)
    fstr = f"{out['iid']} | {out['state']} | {out['title']}"
    print(fstr)
    print(f"Description: {out['description']}")
    print(f"Time Spent: {out['time_stats']['human_total_time_spent']}  Estimated Time: {out['time_stats']['human_time_estimate']}")


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactive", "-i", help="Interactive version of the application", action="store_true")
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


if __name__ == '__main__':
    main()