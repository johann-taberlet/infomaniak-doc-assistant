# Connect external applications to kChat

Source: https://www.infomaniak.com/en/support/faq/2001/connect-external-applications-to-kchat

---

This guide allows you to manage external applications with [kChat](https://infomaniak.com/gtl/kchat) using webhooks.

### Preamble

- A webhook is a method that allows an application to be immediately informed when a particular event occurs in another application, rather than constantly asking this application if something new has happened ("polling").Outgoing webhook: kChat communicates information to other apps when an event occurs in kChat.Incoming webhook: kChat receives information from other apps to trigger actions in kChat.
- It is not possible to import the discussion history from another application (Slack, Teams, Jabber, etc.) or from another Organization.

**⚠ Max. number of incoming/outgoing webhooks:**

## Access the kChat webhooks interface

### Prerequisites

- Not being an external user (this user will not see the menu *Integrations*).

To configure a webhook, find self-hosted or third-party applications and integrations:

1. [Click here‍‍](https://kchat.infomaniak.com/)to access the **kChat** Web app (online service [ksuite.infomaniak.com/kchat](https://ksuite.infomaniak.com/kchat)) or open the **kChat** desktop app (desktop application on macOS / Windows / Linux).
2. Click on the **New** icon ‍ next to your kChat organization's name.
3. Click on **Integrations**.
4. Access the categories:

![image](https://faq.storage5.infomaniak.com/6184238ffe75a7fd22ad0c252392f0fbd0754167.png)

## Integration example

- [Reminder of Infomaniak calendar event on kChat](https://www.infomaniak.com/en/support/faq/2244)

## Create a simple incoming webhook

To do this:

1. Click on the category **Incoming Webhooks**.
2. Click on the blue button **Add incoming webhooks**:

![image](https://faq.storage5.infomaniak.com/a8afd894584a705bee1a7d20f305bf2900c81a14.png)

3. Add a name and a description (max 500 characters) for the webhook.
4. Select the channel that will receive the messages.
5. Save to get the URL (not to be disclosed publicly); example “`https://your-server-kchat.xyz/hooks/xxx-key-generated-xxx`”.

### Webhook usage

On the application that needs to post on kChat:

1. Adjust the code below according to the URL obtained:POST /hooks/xxx-key-generated-xxx HTTP/1.1
Host: your-server-kchat.xyz
Content-Type: application/json
Content-Length: 63
{
    "text": "Hello, text1\nText2."
}
2. Optionally, use the same request but in `curl` (to test from a `Terminal` type application (command line interface, `CLI / Command Line Interface`) on your device): curl -i -X POST -H 'Content-Type: application/json' -d '{"text": "Hello, text1\nText2."}' https://your-server-kchat.xyz/hooks/xxx-key-generated-xxx

If no `Content-Type` header is set, the request body must be preceded by `payload=` like this:

```
payload={"text": "Hello, text1\nText2."}
```

A successful request will receive the following response:

```
HTTP/1.1 200 OK	
Content-Type: application/json	
X-Version-Id: 4.7.1.dev.12799dvd77e172e8a2eba0f4041ec1471.false	
Date: Sun, 01 Jun 2023 17:00:00 GMT	
Content-Length: 58	
	
{	
    "id":"x",	
    "create_at":1713198308869,	
    "update_at":1713198308869,	
    "delete_at":0,	
    "user_id":"x",	
    "channel_id":"x",	
    "root_id":"",	
    "original_id":"",	
    "participants":null,	
    "message":"test",	
    "type":"",	
    "props":{	
        "override_username":"webhook",	
        "override_icon_url":null,	
        "override_icon_emoji":null,	
        "webhook_display_name":"test",	
        "attachments":[	
	
        ],	
        "card":null,	
        "from_webhook":"true"	
    },	
    "hashtags":null,	
    "metadata":{	
        "embeds":[	
            {	
                "type":"message_attachment"	
            }	
        ],	
        "files":[	
	
        ],	
        "reactions":[	
	
        ]	
    },	
    "file_ids":null,	
    "has_reactions":false,	
    "edit_at":0,	
    "is_pinned":false,	
    "remote_id":null,	
    "reply_count":0,	
    "pending_post_id":null,	
    "is_following":false	
}
```

If you want to have the same response format as Slack:

```
HTTP/1.1 200 OK
Content-Type: text/plain
X-Request-Id: hoan69ws7rp5xj7wu9rmystry
X-Version-Id: 4.7.1.dev.12799dvd77e172e8a2eba0f4041ec1471.false
Date: Sun, 01 Jun 2023 17:00:00 GMT
Content-Length: 2
ok
```

you must add `?slack_return_format=true` to the webhook URL.

> **Note:** The BOT indication is added next to the username on kChat for security reasons.

### Settings

In addition to the `text` field, here is the complete list of supported parameters:

### Example code with parameters

Here is how to generate a more complete message with parameters, some of which can replace parameters already set during webhook creation (username, preferred channel, avatar...) as indicated in the table above:

```
POST /hooks/xxx-clé-générée-xxx HTTP/1.1
Host: votre-serveur-kchat.xyz
Content-Type: application/json
Content-Length: 630
{
  "channel": "kchatemp",
  "username": "test-automation",
  "icon_url": "https://domain.xyz/wp-content/uploads/2023/06/icon.png",
  "text": "#### Résultats des tests pour le 27 juillet 2023\n@channel veuillez vérifier les tests échoués.\n\n| Composant  | Tests effectués   | Tests échoués                                   |\n|:-----------|:-----------:|:-----------------------------------------------|\n| Serveur     | 948         |  0                           |\n| Client Web | 123         |  2 [(voir détails)](https://linktologs) |\n| Client iOS | 78          |  3 [(voir détails)](https://linktologs) |"
}
```

This will result in the display of this message in the channel *kchatemp* of the organization:

![sign](https://faq.storage.infomaniak.com/64cd0f7f3139d8.11278371png)