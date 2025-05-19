import os
import re
from github import Github
from datetime import datetime, timedelta, timezone

# Get GitHub token from environment variable
github_token = os.environ.get("GITHUB_TOKEN")
g = Github(github_token)


def get_recent_repos(user, days=30):
    """Get repositories the user has been active in recently"""
    user_obj = g.get_user(user)
    # Create an offset-aware datetime for proper comparison
    recent_date = datetime.now(timezone.utc) - timedelta(days=days)

    # Get user's repositories
    repos = user_obj.get_repos()

    recent_repos = []
    learning_topics = set()

    for repo in repos:
        # Check if repo was updated recently
        if repo.updated_at > recent_date:
            recent_repos.append(repo.name)

            # Extract potential learning topics from repo description and languages
            if repo.description:
                # Look for keywords like "learning", "practicing", "studying" in description
                desc_lower = repo.description.lower()
                if any(word in desc_lower for word in ["learning", "practicing", "studying"]):
                    # Extract the technology being learned
                    for tech in ["kotlin", "python", "javascript", "react", "flutter", "android",
                                 "tensorflow", "pytorch", "ml", "ai", "backend", "frontend", "fullstack"]:
                        if tech in desc_lower:
                            learning_topics.add(tech)

            # Add main language as potential learning topic
            if repo.language and repo.language.lower() not in learning_topics:
                learning_topics.add(repo.language.lower())

    return recent_repos, learning_topics


def update_readme(user):
    """Update the README.md file with current work information"""

    # Get recent activity data
    recent_repos, learning_topics = get_recent_repos(user)

    # Prepare the new current work section
    current_work_lines = []

    # Current projects line based on recent repositories
    if recent_repos:
        repos_str = ", ".join([f"`{repo}`" for repo in recent_repos[:3]])
        current_work_lines.append(f"- 🔭 I'm currently working on {repos_str}")
    else:
        current_work_lines.append(
            "- 🔭 I'm currently working on a financial transaction management app using Flask and Android.")

    # Learning line based on detected topics
    if learning_topics:
        topics_str = ", ".join([topic for topic in learning_topics][:3])
        current_work_lines.append(f"- 🌱 I'm currently learning {topics_str}")
    else:
        current_work_lines.append("- 🌱 I'm currently learning advanced Kotlin and backend optimization techniques.")

    # Keep other static lines
    current_work_lines.extend([
        "- 👯 I'm looking to collaborate on innovative tech projects, especially in the realms of AI and ML.",
        "- 🤔 I'm looking for help with scaling Flask applications.",
        "- 💬 Ask me about full stack development, machine learning, or any of my projects.",
        "- 📫 How to reach me: [Your Contact Information]",
        "- 😄 Pronouns: [Your Pronouns]",
        f"- ⚡ Fun fact: Updated on {datetime.now().strftime('%B %d, %Y')}!"
    ])

    # Read the current README
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        # Create a basic README if it doesn't exist
        content = f"# {user}\n\n<!-- CURRENT-WORK:START -->\n<!-- CURRENT-WORK:END -->"
        print("README.md not found. Creating a basic one.")

    # Replace the current work section
    start_marker = "<!-- CURRENT-WORK:START -->"
    end_marker = "<!-- CURRENT-WORK:END -->"

    new_section = f"{start_marker}\n" + "\n".join(current_work_lines) + f"\n{end_marker}"

    # Find and replace the section using regex
    pattern = f"{re.escape(start_marker)}(.*?){re.escape(end_marker)}"
    
    if re.search(pattern, content, flags=re.DOTALL):
        updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    else:
        # If markers don't exist, append the section
        updated_content = content + f"\n\n{new_section}"
        print("Markers not found in README. Appending section.")

    # Write the updated content back to README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print("README.md updated successfully!")


if __name__ == "__main__":
    # Replace with your GitHub username
    update_readme("imnexerio")
