import pandas as pd

def read_csv(file_path):
    """Read CSV file and return a list of URLs."""
    df = pd.read_csv(file_path, header=None, encoding='utf-8')  # Specify encoding
    return df[0].tolist()  # The URLs are in the first column

def format_as_table(urls):
    """Format a list of URLs as a Markdown table."""
    table_header = '| URL |\n| --- |\n'
    table_rows = '\n'.join([f'| {url} |' for url in urls])
    return table_header + table_rows

def update_readme(readme_path, urls):
    """Update README.md to insert URL table before '## Star History'."""
    # Read the current content of the README
    with open(readme_path, 'r', encoding='utf-8') as file:
        readme_content = file.readlines()

    # Extract existing URLs
    existing_urls = set()
    for line in readme_content:
        if line.startswith('| '):
            parts = line.strip().split('|')
            if len(parts) == 3 and parts[1].strip():
                existing_urls.add(parts[1].strip())

    # Filter out URLs that are already in the README
    new_urls = [url for url in urls if url not in existing_urls]

    if not new_urls:
        print("No new URLs to add.")
        return

    # Format new URLs as a Markdown table
    new_table = format_as_table(new_urls)

    # Find the index to insert the new content
    insert_index = None
    for i, line in enumerate(readme_content):
        if line.startswith('## Star History'):
            insert_index = i
            break

    if insert_index is None:
        raise ValueError("Section '## Star History' not found in README.md")

    # Create new content
    new_content = readme_content[:insert_index] + [new_table + '\n'] + readme_content[insert_index:]

    # Write the updated content back to the README file
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.writelines(new_content)

if __name__ == "__main__":
    csv_file_path = 'repo.csv'
    readme_file_path = 'README.md'

    # Read URLs from CSV
    urls = read_csv(csv_file_path)

    # Update README file
    update_readme(readme_file_path, urls)
