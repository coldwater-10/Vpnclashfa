import re
import urllib.request
import sys

url = 'https://easylist-downloads.adblockplus.org/easylist.txt'
header_pattern = r'^!.*'
comment_pattern = r'^#.*'
whitelist_pattern = r'^@@.*'
blocklist_pattern = r'^\|\|.*\^$'
regex_pattern = r'^\|\|.*\^(\$.*|)'
domain_pattern = r'^\|\|.*\^'
separator = ','

with urllib.request.urlopen(url) as response:
    content = response.read().decode('utf-8')

# Remove headers, comments, and whitelisted domains
content = re.sub(f'{header_pattern}|{comment_pattern}|{whitelist_pattern}', '', content)

# Convert blocklist rules to domain rules
blocklist_domains = [re.sub(f'{blocklist_pattern}', '', rule) for rule in content.split('\n') if re.match(f'{blocklist_pattern}', rule)]
regex_domains = [re.sub(f'{regex_pattern}', '', rule) for rule in content.split('\n') if re.match(f'{regex_pattern}', rule)]
domain_rules = sorted(set(blocklist_domains + regex_domains))

# Write domains to file in Clash config format
with open(sys.argv[1], 'w') as f:
    for domain in domain_rules:
        if re.match(f'{domain_pattern}', domain):
            f.write(f'- DOMAIN-SUFFIX,{domain.strip("|")}\n')
        else:
            f.write(f'- DOMAIN,{domain.strip("|")}\n')
