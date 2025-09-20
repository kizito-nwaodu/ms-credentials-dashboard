
import requests
import datetime

# Define the Microsoft Learn Catalog API endpoint
API_URL = "https://learn.microsoft.com/api/catalog/"

# Define the output HTML file name
HTML_FILE = "ms_credentials_dashboard.html"

# Function to fetch catalog data from Microsoft Learn
def fetch_catalog():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

# Function to filter newly added items from the last 30 days
def filter_new_items(items):
    new_items = []
    today = datetime.datetime.utcnow()
    for item in items:
        if "publishedDate" in item:
            try:
                published_date = datetime.datetime.strptime(item["publishedDate"], "%Y-%m-%dT%H:%M:%SZ")
                if (today - published_date).days <= 30:
                    new_items.append(item)
            except ValueError:
                continue
    return new_items

# Function to generate HTML dashboard
def generate_html(certifications, applied_skills):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Microsoft Credentials Dashboard</title>
    <meta http-equiv="refresh" content="21600"> <!-- Auto-refresh every 6 hours -->
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; }}
        ul {{ line-height: 1.6; }}
        .section {{ margin-bottom: 40px; }}
        footer {{ margin-top: 60px; font-size: 0.9em; color: #7f8c8d; }}
    </style>
</head>
<body>
    <h1>🧠 Microsoft Credentials Dashboard</h1>
    <p>Last updated: {timestamp}</p>

    <div class="section">
        <h2>🆕 Newly Added Certifications (Last 30 Days)</h2>
        <ul>
"""
    for cert in certifications:
        html += f'<li><a href="{cert.get("url", "#")}" target="_blank">{cert.get("title", "Untitled")}</a></li>
'

    html += """
        </ul>
    </div>

    <div class="section">
        <h2>🆕 Newly Added Applied Skills (Last 30 Days)</h2>
        <ul>
"""
    for skill in applied_skills:
        html += f'<li><a href="{skill.get("url", "#")}" target="_blank">{skill.get("title", "Untitled")}</a></li>
'

    html += f"""
        </ul>
    </div>

    <footer>
        Data sourced from <a href="https://learn.microsoft.com/en-us/credentials/" target="_blank">Microsoft Learn</a>.
        This dashboard auto-refreshes every 6 hours.
    </footer>
</body>
</html>
"""
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

# Main execution
def main():
    catalog = fetch_catalog()
    certifications = [item for item in catalog if item.get("type") == "certification"]
    applied_skills = [item for item in catalog if item.get("type") == "appliedSkill"]

    new_certifications = filter_new_items(certifications)
    new_applied_skills = filter_new_items(applied_skills)

    generate_html(new_certifications, new_applied_skills)

# Run the script
if __name__ == "__main__":
    main()
