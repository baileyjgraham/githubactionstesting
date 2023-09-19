import os
from datetime import datetime
from github import Github

def calculate_duration(card):
    created_at = card.created_at
    now = datetime.utcnow()
    duration = (now - created_at).days + 1
    return duration

def main():
    github_token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("GITHUB_REPOSITORY")

    g = Github(github_token)
    repo = g.get_repo(repo_name)

    column_name = "code review"  # update with column name when I can create projects
    label_prefix = "Day[s]: "

    project = repo.get_projects()[0]  # Assuming there's only one project board

    for column in project.get_columns():
        if column.name.lower() == column_name.lower():
            for card in column.get_cards():
                issue = card.get_content()
                if issue and issue.pull_request is None:
                    continue  # Skip non-issue cards

                duration = calculate_duration(card)
                label_name = label_prefix + str(duration)

                # Remove existing label with the same prefix
                for label in issue.get_labels():
                    if label.name.startswith(label_prefix):
                        issue.remove_from_labels(label)

                # Add/update the label
                issue.add_to_labels(label_name)
        else:
            # Handle label removal when moving to the next column
            for card in column.get_cards():
                issue = card.get_content()
                if issue and issue.pull_request is None:
                    continue  # Skip non-issue cards

                # Remove labels with the prefix
                for label in issue.get_labels():
                    if label.name.startswith(label_prefix):
                        issue.remove_from_labels(label)

if __name__ == "__main__":
    main()
