# Rule Engine

This project is a standalone Python script that interacts with the Gmail API to fetch emails, store them in a PostgreSQL database, and process them based on defined rules.

## Features

- Authenticate to Gmail API using OAuth.
- Fetch and store emails in a PostgreSQL database.
- Process emails based on rules defined in a JSON file.
- Mark emails as read/unread and move them based on rules.

## Requirements

- Python 3.9 or higher
- PostgreSQL
- Required Python libraries (listed in `requirements.txt`)

## Setup

### Clone the Repository

```bash
git clone <repository-url>
cd RuleEngine
```

### Create and Activate a Virtual Environment

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set `PYTHONPATH`

```bash
export PYTHONPATH=${PYTHONPATH}:${HOME}/path_to_cloned_repo/RuleEngine/rule_engine 
```

### Configure the Database

1. Create a PostgreSQL database and user.
2. Update the data/db_config.json file with your database configuration:

```bash
{
  "dbname": "your_db_name",
  "user": "your_db_user",
  "password": "your_db_password",
  "host": "your_db_host",
  "port": "your_db_port"
}
```


### Google OAuth Setup

use this to link to setup https://support.google.com/googleapi/answer/6158849

### Rules Configuration

Define your rules in the data/test_rules.json file. Here is an example:

```bash
{
    "rule_sets": [
        {
            "predicate": "Any",
            "rules": [
                {"field": "from_email", "predicate": "contains", "value": "google.com"},
                {"field": "to_email", "predicate": "contains", "value": "myemail@gmail.com"},
                {"field": "subject", "predicate": "contains", "value": "google"}
            ],
            "actions": [
                {"action": "mark_as_read"}
            ]
        },
        {
            "predicate": "All",
            "rules": [
                {"field": "from_email", "predicate": "contains", "value": "swiggy"},
                {"field": "to_email", "predicate": "contains", "value": "myemail@gmail.com"},
                {"field": "subject", "predicate": "contains", "value": "Food"}
                {"field": "received_date", "predicate": "less than", "value": "14"}
            ],
            "actions": [
                {"action": "mark_as_unread"},
                {"action": "move_message", "params": {"label_id": "TRASH"}}
            ]
        }
    ]
}

```


## Running the Application

### Fetch and Write Emails

This function fetches emails from the Gmail server and stores them in the database.



```bash
fetch_and_write_emails()
python rule_engine/main.py
```

### Process Rules on Emails

This function processes the emails stored in the database based on the defined rules.

```bash
process_rules_on_emails()
python rule_engine/main.py
```


## Notes
Ensure you have the appropriate permissions and credentials to access the Gmail API.
Customize the rules in test_rules.json as per your requirements.