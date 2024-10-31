import requests
import csv

token = "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"
headers = {'Authorization': f'token {token}'}
url = 'https://api.github.com/search/users?q=location:Sydney+followers:>100'

# Make the API request
response = requests.get(url, headers=headers)

# Print the response status code and JSON for debugging
print(f'Status Code: {response.status_code}')
print('Response JSON:', response.json)

# Check if the request was successful
if response.status_code == 200:
    users_data = response.json().get('items', [])
    
    # Prepare user data
    users = []
    for user in users_data:
        users.append({
            'login': user['login'],
            'name': user.get('name', ''),
            'company': user.get('company', '').strip('@').upper(),
            'location': user.get('location', ''),
            'email': user.get('email', ''),
            'hireable': user.get('hireable', ''),
            'bio': user.get('bio', ''),
            'public_repos': user['public_repos'],
            'followers': user['followers'],
            'following': user['following'],
            'created_at': user['created_at'],
        })

    # Write users to CSV
    with open('users.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)

    # Fetch repositories for each user
    repositories = []
    for user in users:
        repos_url = f'https://api.github.com/users/{user["login"]}/repos?per_page=500'
        repos_response = requests.get(repos_url, headers=headers)
        
        # Check if the request was successful
        if repos_response.status_code == 200:
            repos_data = repos_response.json()

            for repo in repos_data:
                repositories.append({
                    'login': user['login'],
                    'full_name': repo['full_name'],
                    'created_at': repo['created_at'],
                    'stargazers_count': repo['stargazers_count'],
                    'watchers_count': repo['watchers_count'],
                    'language': repo['language'],
                    'has_projects': repo.get('has_projects', False),
                    'has_wiki': repo.get('has_wiki', False),
                    'license_name': repo['license']['key'] if repo.get('license') else '',
                })

    # Write repositories to CSV
    with open('repositories.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=repositories[0].keys())
        writer.writeheader()
        writer.writerows(repositories)

else:
    print('Failed to retrieve users:', response_json.get('message', 'No error message'))
        writer.writerows(repositories)

else:
    print('Failed to retrieve users:', response.json())
